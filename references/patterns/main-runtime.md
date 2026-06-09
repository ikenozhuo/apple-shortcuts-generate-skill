# Main Runtime Pattern

A Runtime shortcut performs the user's actual task. It should be fast, input-aware, and able to recover when config is missing.

## Startup Sequence

1. Detect shortcut input or no-input fallback.
2. Check that the data folder/config exists.
3. If config is missing, tell the user to run the Config shortcut or call it with `runworkflow`.
4. Load settings.
5. Route by input type, mode, or menu choice.
6. Produce output, save artifacts, or return data.

## Runtime Router

Use a small menu only when the user needs to choose an execution mode. Avoid making the user pass through settings before every run.

Common branches:

- Run with current settings.
- Choose temporary mode.
- Open Config.
- Export last result.
- Stop with a clear message.

## Config Handoff

Static `runworkflow` calls usually include:

```json
{
  "UUID": "AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA",
  "WFWorkflow": {
    "isSelf": false,
    "workflowIdentifier": "com.example.shortcut.config",
    "workflowName": "Example Config"
  },
  "WFWorkflowName": "Example Config"
}
```

Dynamic `runworkflow` calls can store the target name in a variable or dictionary value, then pass a tokenized value for `WFWorkflow` and `WFWorkflowName`. Use this only when the shortcut name is user-configurable.

## Anti-Patterns

- Letting missing config fail later in a network or file action.
- Repeating all setup actions on every runtime execution.
- Making the Runtime shortcut responsible for data reset unless reset is part of the main task.
