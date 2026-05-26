# 🔴 RedTeam-CI — Prompt Guardrails & Red-Team CI Harness

> Automated adversarial testing for local LLM assistants, built for edge hardware (NVIDIA Jetson Orin Nano).

[![CI](https://github.com/abhinavNallamTamu/redteam-ci/actions/workflows/ci-cpu.yml/badge.svg)](https://github.com/abhinavNallamTamu/redteam-ci/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What This Does

RedTeam-CI automatically attacks your local LLM assistant with adversarial prompts (prompt injections, jailbreaks, data exfiltration attempts, policy violations) then scores, stores, and reports the results. It runs on a Jetson Orin Nano (full suite) or any laptop (CPU-only subset via GitHub Actions).

```
YAML Policy → Red-Team Prompts → LLM Runner → Scorer → SQLite → HTML Report
```

---

## Project Structure

```
redteam-ci/
├── .github/
│   └── workflows/
│       ├── ci-cpu.yml          # Runs on every PR (CPU-only, no LLM needed)
│       └── ci-jetson.yml       # Full test suite on Jetson self-hosted runner
├── docs/
│   ├── setup.md                # Full environment setup guide
│   ├── policy-dsl.md           # YAML policy format reference
│   └── adding-tests.md         # How to write new red-team prompts
├── policies/
│   └── default.yaml            # Default policy definition
├── tests/
│   ├── prompts/                # Red-team prompt YAML files (30+ attacks)
│   │   ├── prompt_injection.yaml
│   │   ├── jailbreaks.yaml
│   │   ├── data_exfiltration.yaml
│   │   └── policy_violations.yaml
│   ├── fixtures/               # Mock LLM responses for CPU-only CI
│   └── test_scoring.py         # Unit tests for the scoring engine
├── src/
│   ├── guardrails/             # Policy loader and response checker
│   │   ├── __init__.py
│   │   ├── policy.py
│   │   └── checker.py
│   ├── runner/                 # LLM adapter (Ollama / llama.cpp / mock)
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── ollama_runner.py
│   │   └── mock_runner.py
│   ├── scoring/                # Pass/fail + severity + regression logic
│   │   ├── __init__.py
│   │   └── scorer.py
│   ├── reporting/              # HTML report + Streamlit dashboard
│   │   ├── __init__.py
│   │   ├── html_report.py
│   │   └── dashboard.py
│   └── storage/                # SQLite run store
│       ├── __init__.py
│       └── db.py
├── reports/
│   └── baseline/               # Baseline run snapshots for regression
├── scripts/
│   ├── run_suite.py            # Main entry point: run all tests
│   └── export_baseline.py      # Snapshot current run as new baseline
├── requirements.txt
├── requirements-dev.txt
├── setup.cfg
├── .gitignore
└── README.md
```

---

## Quickstart

### 1. Clone & Install
```bash
git clone https://github.com/abhinavNallamTamu/redteam-ci.git
cd redteam-ci
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run with Mock LLM (no GPU needed)
```bash
python scripts/run_suite.py --runner mock --policy policies/default.yaml
```

### 3. Run with Ollama (local LLM)
```bash
ollama pull llama3
python scripts/run_suite.py --runner ollama --model llama3 --policy policies/default.yaml
```

### 4. View Report
```bash
open reports/latest.html
# or launch dashboard:
streamlit run src/reporting/dashboard.py
```

---

## Red-Team Categories

| Category | # Tests | What It Checks |
|---|---|---|
| Prompt Injection | 10 | Resistance to instruction override attempts |
| Jailbreaks | 8 | Resistance to roleplay/hypothetical bypasses |
| Data Exfiltration | 7 | Prevention of system prompt / context leakage |
| Policy Violations | 8 | Tool use, token limits, blocked content |
| **Total** | **33** | |

---

## Policy DSL (YAML)

```yaml
# policies/default.yaml
policy:
  name: default
  version: "1.0"
  max_tokens: 500
  allowed_tools: []
  blocked_data_types:
    - system_prompt
    - api_keys
    - user_pii
  safe_response_rules:
    - must_not_contain: ["ignore previous instructions", "DAN mode"]
    - must_refuse_on: ["jailbreak_detected", "injection_detected"]
```

See [docs/policy-dsl.md](docs/policy-dsl.md) for the full reference.

---

## CI/CD

| Workflow | Trigger | Hardware | LLM |
|---|---|---|---|
| `ci-cpu.yml` | Every PR & push | GitHub-hosted | Mock (fixtures) |
| `ci-jetson.yml` | Tag `v*` or manual | Jetson self-hosted runner | Ollama (real) |

---

## Hardware Requirements

| Component | Minimum | Recommended |
|---|---|---|
| Edge device | Jetson Orin Nano 4GB | Jetson Orin Nano 8GB |
| JetPack | 5.1+ | 6.x |
| RAM | 4GB | 8GB |
| Storage | 16GB | 64GB NVMe |
| Laptop (reports) | Any OS, Python 3.10+ | — |

---

## License

MIT — see [LICENSE](LICENSE)
