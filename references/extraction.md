# Extracting Plaintext from Signed Shortcuts

Convert a signed `.shortcut` file back into readable XML plist.

## When You Need This

- You exported a shortcut from Shortcuts.app and got a signed `.shortcut` file
- You want to inspect, edit, or reverse-engineer an existing shortcut
- `plutil -convert xml1` fails with "Unexpected character" because the file starts with `AEA1`

## The AEA1 Format

Modern `.shortcut` files (iOS 16.4+, macOS 13.3+) use **Apple Encrypted Archive (AEA)** with **Profile 0**:

| Feature | Status |
|---------|--------|
| Encryption | None (plaintext payload) |
| Signing | ECDSA-P256 signature |
| Compression | LZFSE inside an Apple Archive |

File structure:

| Offset | Field |
|--------|-------|
| 0x00 | Magic `AEA1` |
| 0x04 | Profile ID (3 bytes) + scrypt hardness (1 byte) |
| 0x08 | Auth data length (4 bytes, little-endian) |
| 0x0C | Auth data (`bplist00` containing certificate chain) |
| ... | Prologue signature (128 bytes) |
| ... | Encrypted payload (Profile 0 = cleartext, just compressed) |

The actual shortcut workflow is an Apple Archive inside the payload.

## Extraction Steps

### Step 1: Extract auth data and get the signing public key

The auth data length is at offset 0x08 (little-endian).

```bash
# 1. Extract auth data bplist
AUTH_LEN=$(xxd -l 4 -s 8 -e input.shortcut | awk '{print $2}')
dd if=input.shortcut of=authdata.bplist bs=1 skip=12 count=$AUTH_LEN

# 2. Convert to XML
plutil -convert xml1 authdata.bplist -o authdata.plist

# 3. Extract the first (leaf) certificate
plutil -extract SigningCertificateChain.0 raw authdata.plist -o cert.b64
base64 -D -i cert.b64 -o cert.der

# 4. Extract the ECDSA public key
openssl x509 -in cert.der -inform DER -pubkey -noout > sign-pub.pem
```

### Step 2: Decrypt (verify + extract) the AEA payload

```bash
aea decrypt -sign-pub sign-pub.pem -i input.shortcut -o payload.aar
```

This produces an **Apple Archive** (`payload.aar`).

### Step 3: Extract the Apple Archive

```bash
aa extract -i payload.aar -d extracted/
```

The archive typically contains a single file: `Shortcut.wflow` (binary plist).

### Step 4: Convert to XML plaintext

```bash
plutil -convert xml1 extracted/Shortcut.wflow -o output.plist
```

Now `output.plist` is the fully readable, unencrypted shortcut definition.

## Bundled Script

Prefer the skill's bundled script for routine extraction:

```bash
python3 scripts/extract_shortcut.py MomoTodo.shortcut --output MomoTodo_plaintext.plist
```

Use `--keep-workdir debug-dir` to keep auth data, certificate, payload, and extracted archive files for troubleshooting.

## Manual Script Pattern

```bash
#!/bin/bash
set -e

INPUT="$1"
BASENAME="${INPUT%.shortcut}"

# Extract auth data length
AUTH_LEN=$(xxd -l 4 -s 8 -e "$INPUT" | awk '{print $2}')

# Extract and convert auth data
dd if="$INPUT" of="${BASENAME}_authdata.bplist" bs=1 skip=12 count=$AUTH_LEN 2>/dev/null
plutil -convert xml1 "${BASENAME}_authdata.bplist" -o "${BASENAME}_authdata.plist" 2>/dev/null

# Get public key from certificate
plutil -extract SigningCertificateChain.0 raw "${BASENAME}_authdata.plist" -o "${BASENAME}_cert.b64" 2>/dev/null
base64 -D -i "${BASENAME}_cert.b64" -o "${BASENAME}_cert.der"
openssl x509 -in "${BASENAME}_cert.der" -inform DER -pubkey -noout > "${BASENAME}_sign-pub.pem"

# Decrypt AEA
aea decrypt -sign-pub "${BASENAME}_sign-pub.pem" -i "$INPUT" -o "${BASENAME}_payload.aar"

# Extract Apple Archive
mkdir -p "${BASENAME}_extracted"
aa extract -i "${BASENAME}_payload.aar" -d "${BASENAME}_extracted"

# Convert to XML
plutil -convert xml1 "${BASENAME}_extracted/Shortcut.wflow" -o "${BASENAME}_plaintext.plist"

echo "Done: ${BASENAME}_plaintext.plist"
```

Usage:
```bash
chmod +x extract_shortcut.sh
./extract_shortcut.sh MomoTodo.shortcut
```

## Requirements

- macOS Monterey+ (provides `aea`, `aa`, `shortcuts` CLI)
- `openssl` (pre-installed on macOS)
- `plutil` (pre-installed on macOS)

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `plutil: Unexpected character A at line 1` | File is AEA1, not raw plist | Follow extraction steps above |
| `aea: -sign-pub is required` | Missing public key for verification | Extract from auth data certificate chain |
| `base64: invalid argument` | Using GNU `base64` syntax on macOS | Use `base64 -D -i file -o out` |
| `Shortcut.wflow` not found | Wrong `aa extract` target option or unexpected archive path | Use `aa extract -i payload.aar -d extracted/` and check `aa list -i payload.aar` |

## Re-Signing After Editing

Once you edit the XML and want to use it again:

```bash
# Convert back to binary (optional)
plutil -convert binary1 output.plist -o edited.shortcut

# Sign for import
shortcuts sign --mode anyone --input edited.shortcut --output edited_signed.shortcut
```

## References

- [plist-format.md](plist-format.md) - Plist structure and keys
- [Apple Encrypted Archive](https://theapplewiki.com/wiki/Apple_Encrypted_Archive)
- [kinnay/AEA](https://github.com/kinnay/AEA) - Cross-platform Python decoder
