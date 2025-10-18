# AI Code Review Lite

Turn a git diff (or your whole repository) into a **ranked risk report** that blends:
- **Security findings** (Bandit)
- **Style/quality issues** (Flake8)
- **Complexity signals** (Radon)

Outputs a tidy **`report.md`** you can attach to pull requests or releases.

![license](https://img.shields.io/badge/license-MIT-blue)

---

## 1) Prerequisites (developers)
- Python **3.11+**
- Git
- (Optional) Docker
- (Optional) Make

> Windows users: examples below show **PowerShell** and **CMD** variants where needed.

---

## 2) Get the code
```bash
# HTTPS
git clone https://github.com/<owner>/<repo>.git
cd <repo>
```
```bash
# SSH (optional)
git clone git@github.com:<owner>/<repo>.git
cd <repo>
```

---

## 3) Set up a local environment

### Option A — No virtualenv (quickest)
```bash
pip install -r requirements.txt
```

### Option B — Virtualenv (recommended)
**macOS/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
**Windows PowerShell**
```powershell
py -3 -m venv .venv
. .venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

---

## 4) Run tests
```bash
pytest -q
```
Expected: tests pass; artifacts are not created here.

---

## 5) Generate a local report

### 5.1 Review last commit (git diff)
```bash
python review.py --range HEAD~1..HEAD --output report.md
```

### 5.2 Scan the entire repo (recommended for first run)
```bash
python review.py --all --output report.md
```

> Open **report.md** to view the ranked issues.

---

## 6) Docker usage (no host Python required)

### Build the image
```bash
docker build -t aicrl:local .
```

### Run the container against the current working directory

**Windows PowerShell**
```powershell
docker run --rm -v "${PWD}:/app" -w /app aicrl:local --all --output report.md
```
**Windows CMD**
```cmd
docker run --rm -v "%cd%:/app" -w /app aicrl:local --all --output report.md
```
**macOS/Linux**
```bash
docker run --rm -v "$PWD:/app" -w /app aicrl:local --all --output report.md
```

---

## 7) CI/CD (GitHub Actions)

### CI on every push/PR
- Install deps
- Run tests
- Generate **report.md**
- Upload **report.md** as a build artifact

Workflow excerpt (`.github/workflows/ci.yml`):
```yaml
- run: pytest -q
- run: python review.py --all --output report.md
- uses: actions/upload-artifact@v4
  with:
    name: code-review-report
    path: report.md
```

### Release on tag (optional)
- Tag `vX.Y.Z` → publish Release with `report.md`
- Build & push container image to GHCR

Workflow excerpt (`.github/workflows/release.yml`):
```yaml
on:
  push:
    tags: ["v*"]
```

---

## 8) Project layout
```
analyzers/
  __init__.py
  run_tools.py   # adapters for flake8/bandit/radon
  aggregate.py   # ranking & markdown rendering
tests/
  conftest.py    # adds repo root to PYTHONPATH
  test_aggregate.py
  test_integration.py
examples/
  withbugs.py    # intentionally insecure/noisy sample
review.py        # CLI entry point
```

---

## 9) Configuration
- **Flake8 rules:** `.flake8`
- **Bandit rules:** `.bandit`
- **Adjust line length & ignores** to your team’s style.

---

## 10) Troubleshooting

### "No changed Python files in range"
Use a wider range or full scan:
```bash
python review.py --range HEAD~10..HEAD --output report.md
# or
python review.py --all --output report.md
```

### Docker volume mount errors on Windows
Use the correct syntax for your shell:
- PowerShell: `-v "${PWD}:/app"`
- CMD: `-v "%cd%:/app"`
- macOS/Linux: `-v "$PWD:/app"`

### Git not found inside the container
Either install git in the image (see Dockerfile) or run with `--all` to scan the repo without git.

---

## 11) Make targets (optional)
```make
make setup    # pip install -r requirements.txt
make lint     # flake8
make test     # pytest
make run      # python review.py --all --output report.md
make docker   # docker build -t aicrl:local .
```

---

## 12) Roadmap
- SARIF output for GitHub Code Scanning
- Inline PR comments (GitHub App)
- LLM hints for top‑N issues (off by default)
- Language plugins (ESLint, Trivy for Dockerfiles)

---

## 13) License
MIT (see `LICENSE.md`).
