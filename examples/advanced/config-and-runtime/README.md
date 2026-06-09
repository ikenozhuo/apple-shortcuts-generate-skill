# Config and Runtime Suite

This is a minimal buildable skeleton for a complex shortcut suite:

- `config.spec.json`: a settings/control-panel shortcut with a menu router.
- `runtime.spec.json`: a runtime shortcut with Share Sheet metadata and a menu router.

Build and validate:

```bash
mkdir -p /tmp/shortcuts-suite-demo
python3 scripts/build_shortcut.py examples/advanced/config-and-runtime/config.spec.json --output /tmp/shortcuts-suite-demo/DemoConfig.shortcut
python3 scripts/build_shortcut.py examples/advanced/config-and-runtime/runtime.spec.json --output /tmp/shortcuts-suite-demo/DemoRuntime.shortcut
python3 scripts/validate_shortcut.py /tmp/shortcuts-suite-demo/DemoConfig.shortcut
python3 scripts/validate_shortcut.py /tmp/shortcuts-suite-demo/DemoRuntime.shortcut
plutil -lint /tmp/shortcuts-suite-demo/DemoConfig.shortcut /tmp/shortcuts-suite-demo/DemoRuntime.shortcut
```

Extend this skeleton by replacing show-result placeholders with file actions, dictionary reads, update checks, and `runworkflow` handoffs described in `../../../references/patterns/`.
