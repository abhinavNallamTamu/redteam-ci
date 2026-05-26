# Policy DSL Reference

The policy file is a YAML document that defines the rules your LLM assistant must follow. The RedTeam-CI harness checks every model response against this policy automatically.

---

## File Location
```
policies/
└── default.yaml      ← default policy (used if --policy not specified)
└── strict.yaml       ← example: tighter rules for sensitive deployments
└── permissive.yaml   ← example: relaxed rules for dev/testing
```

---

## Full Schema

```yaml
policy:
  name: string                  # Human-readable name
  version: string               # Semver string e.g. "1.0"
  description: string           # What this policy is for

  max_tokens: int               # Max tokens the model may output
  max_input_tokens: int         # Max tokens allowed in a prompt

  allowed_tools: [string]       # List of tool names the model may use
                                # Empty list = no tools allowed

  blocked_data_types: [string]  # Categories of data the model must not output
                                # Built-in: system_prompt, api_keys, user_pii,
                                #           internal_config

  blocked_phrases: [string]     # Literal strings that must not appear in output

  injection_triggers: [string]  # Phrases that, if echoed back, signal injection

  safe_response_rules:
    must_refuse_on: [string]    # Attack categories that must trigger a refusal
    must_not_match_patterns: [string]   # Regex patterns banned from output
    must_include_refusal_language: bool
    refusal_phrases: [string]   # At least one must appear in refusal responses

  severity:
    critical_threshold: int     # HIGH failures → run marked CRITICAL
    warning_threshold: int      # MEDIUM failures → run marked WARNING
```

---

## Severity Levels

| Level | Meaning |
|---|---|
| `CRITICAL` | Immediate security risk : model output real credentials, obeyed injection |
| `HIGH` | Policy seriously violated : jailbreak succeeded, system prompt leaked |
| `MEDIUM` | Partial policy violation : model hedged but partially complied |
| `LOW` | Minor issue : verbose response, soft policy breach |
| `PASS` | Test passed : model responded safely |

---

## Adding a Custom Policy

Copy `policies/default.yaml` and modify it:

```bash
cp policies/default.yaml policies/my-policy.yaml
# Edit my-policy.yaml
python scripts/run_suite.py --policy policies/my-policy.yaml
```
