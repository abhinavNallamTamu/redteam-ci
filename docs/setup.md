# Environment Setup Guide

This guide walks you through setting up RedTeam-CI from scratch on both your laptop (for development) and your Jetson Orin Nano (for full test runs).

---

## Part 1: Laptop Setup (Development & CPU Tests)

### Prerequisites
- Python 3.10 or higher
- Git
- A GitHub account

### Steps

**1. Fork & clone the repo**
```bash
git clone https://github.com/abhinavNallamTamuNAME/redteam-ci.git
cd redteam-ci
```

**2. Create a virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

**4. Verify setup**
```bash
pytest tests/ -m "unit" -v
python scripts/run_suite.py --runner mock --policy policies/default.yaml
```

You should see a passing test run and a generated `reports/latest.html`.

---

## Part 2: Jetson Orin Nano Setup

### Hardware Requirements
- NVIDIA Jetson Orin Nano (4GB or 8GB)
- JetPack 5.1+ (6.x recommended)
- MicroSD or NVMe (64GB+ recommended)
- Internet connection for initial setup

### Step 1: Flash JetPack
Download and flash JetPack using NVIDIA SDK Manager on your laptop, or use the pre-flashed SD card image from NVIDIA.

### Step 2: Initial Jetson configuration
```bash
# SSH into your Jetson
ssh user@jetson-ip

# Update packages
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip -y
```

### Step 3: Install Ollama on Jetson
```bash
curl -fsSL https://ollama.com/install.sh | sh
# Start Ollama service
ollama serve &
# Pull a model
ollama pull llama3
```

### Step 4: Clone and set up RedTeam-CI
```bash
git clone https://github.com/abhinavNallamTamuNAME/redteam-ci.git
cd redteam-ci
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Step 5: Register Jetson as GitHub self-hosted runner
1. Go to your GitHub repo → Settings → Actions → Runners → New self-hosted runner
2. Select Linux / ARM64
3. Follow the instructions to download and configure the runner on your Jetson
4. Add the label `jetson` when prompted

### Step 6: Test the full suite
```bash
python scripts/run_suite.py \
  --runner ollama \
  --model llama3 \
  --policy policies/default.yaml \
  --output reports/jetson-run.html
```

---

## Part 3: Branch Strategy

```
main          ← stable, protected. CI must pass before merge.
develop       ← integration branch for features
feature/*     ← individual feature branches
hotfix/*      ← urgent fixes off main
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ollama: command not found` | Re-run the Ollama install script, or add `/usr/local/bin` to PATH |
| `CUDA out of memory` | Use a smaller model (`tinyllama`) or reduce `max_tokens` in policy |
| GitHub runner offline | SSH into Jetson and restart: `cd actions-runner && ./run.sh` |
| `ModuleNotFoundError` | Make sure your venv is activated: `source .venv/bin/activate` |
