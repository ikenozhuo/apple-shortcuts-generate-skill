#!/usr/bin/env python3
"""Extract a signed AEA1 .shortcut file to readable XML plist."""

from __future__ import annotations

import argparse
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise RuntimeError(f"required tool not found: {name}")


def read_auth_data(input_path: Path) -> bytes:
    data = input_path.read_bytes()
    if not data.startswith(b"AEA1"):
        raise ValueError("input does not start with AEA1; try plutil -convert xml1")
    if len(data) < 12:
        raise ValueError("input is too small to contain AEA auth data")
    auth_len = struct.unpack("<I", data[8:12])[0]
    end = 12 + auth_len
    if end > len(data):
        raise ValueError("AEA auth data length exceeds file size")
    return data[12:end]


def extract(input_path: Path, output_path: Path, workdir: Path) -> None:
    for tool in ("plutil", "base64", "openssl", "aea", "aa"):
        require_tool(tool)

    auth_bplist = workdir / "authdata.bplist"
    auth_plist = workdir / "authdata.plist"
    cert_b64 = workdir / "cert.b64"
    cert_der = workdir / "cert.der"
    sign_pub = workdir / "sign-pub.pem"
    payload = workdir / "payload.aar"
    extracted = workdir / "extracted"

    auth_bplist.write_bytes(read_auth_data(input_path))
    run(["plutil", "-convert", "xml1", str(auth_bplist), "-o", str(auth_plist)])
    run(
        [
            "plutil",
            "-extract",
            "SigningCertificateChain.0",
            "raw",
            str(auth_plist),
            "-o",
            str(cert_b64),
        ]
    )
    run(["base64", "-D", "-i", str(cert_b64), "-o", str(cert_der)])
    with sign_pub.open("wb") as handle:
        subprocess.run(
            [
                "openssl",
                "x509",
                "-in",
                str(cert_der),
                "-inform",
                "DER",
                "-pubkey",
                "-noout",
            ],
            check=True,
            stdout=handle,
        )
    run(
        [
            "aea",
            "decrypt",
            "-sign-pub",
            str(sign_pub),
            "-i",
            str(input_path),
            "-o",
            str(payload),
        ]
    )
    extracted.mkdir(parents=True, exist_ok=True)
    run(["aa", "extract", "-i", str(payload), "-d", str(extracted)])

    workflow = extracted / "Shortcut.wflow"
    if not workflow.exists():
        candidates = sorted(extracted.rglob("*.wflow"))
        if not candidates:
            raise FileNotFoundError(
                f"Shortcut.wflow not found under {extracted}; inspect with aa list"
            )
        workflow = candidates[0]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    run(["plutil", "-convert", "xml1", str(workflow), "-o", str(output_path)])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract plaintext XML plist from a signed .shortcut file."
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", "-o", type=Path, required=True)
    parser.add_argument(
        "--keep-workdir",
        type=Path,
        help="Keep intermediate files in this directory for debugging",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.keep_workdir:
            args.keep_workdir.mkdir(parents=True, exist_ok=True)
            extract(args.input, args.output, args.keep_workdir)
            print(f"Kept workdir {args.keep_workdir}")
        else:
            with tempfile.TemporaryDirectory(prefix="shortcut-extract-") as tmp:
                extract(args.input, args.output, Path(tmp))
        print(f"Wrote {args.output}")
    except (
        OSError,
        RuntimeError,
        ValueError,
        FileNotFoundError,
        subprocess.CalledProcessError,
    ) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
