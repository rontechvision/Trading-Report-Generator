# Installation & Usage Guide

## 1. Install the Package

The package lives at
[github.com/rontechvision/Trading-Report-Generator](https://github.com/rontechvision/Trading-Report-Generator).
Pick one of the paths below depending on whether you want the `trading-report`
CLI and `skills.report_generator` module available everywhere on your
machine, or scoped to a single project's virtual environment.

### Option A — Global install (available in every project / any shell)

Use this if you want the `trading-report` CLI on your `PATH` system-wide,
independent of any project's virtualenv.

**Recommended: [pipx](https://pipx.pypa.io/)** (isolates the package in its
own environment, only exposes the CLI entry point):

```bash
pipx install git+https://github.com/rontechvision/Trading-Report-Generator.git
```

**Alternative: pip with `--user`** (installs into your user site-packages,
also exposes the `skills.report_generator` module for `import` from any
script run with your global Python):

```bash
pip install --user git+https://github.com/rontechvision/Trading-Report-Generator.git
```

Verify either install:

```bash
trading-report --version
```

To upgrade later, re-run the same command with `--force` (pipx) or
`--upgrade` (pip):

```bash
pipx install --force git+https://github.com/rontechvision/Trading-Report-Generator.git
# or
pip install --user --upgrade git+https://github.com/rontechvision/Trading-Report-Generator.git
```

### Option B — Project-specific install (scoped to one project's venv)

Use this if a specific project depends on `trading-report-generator` and you
want the version pinned/isolated per-project (recommended for reproducible
builds).

1. Activate that project's virtual environment:
   ```bash
   # from the target project's root
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # macOS/Linux
   ```
2. Install straight from GitHub:
   ```bash
   pip install git+https://github.com/rontechvision/Trading-Report-Generator.git
   ```
3. Or pin to a branch, tag, or commit for reproducibility:
   ```bash
   pip install git+https://github.com/rontechvision/Trading-Report-Generator.git@master
   pip install git+https://github.com/rontechvision/Trading-Report-Generator.git@v0.1.0
   pip install git+https://github.com/rontechvision/Trading-Report-Generator.git@<commit-sha>
   ```
4. Or add it to that project's `requirements.txt` so it installs with the
   rest of the project's dependencies:
   ```
   trading-report-generator @ git+https://github.com/rontechvision/Trading-Report-Generator.git@master
   ```
   ```bash
   pip install -r requirements.txt
   ```

### Option C — Editable install (contributing to this repo)

Clone the repo and install it in editable mode so local edits take effect
immediately without reinstalling:

```bash
git clone https://github.com/rontechvision/Trading-Report-Generator.git
cd Trading-Report-Generator
pip install -e .
```

## 2. Configure Figma Credentials

Create a `.env` file in your project root:

```env
FIGMA_TOKEN=your_figma_personal_access_token_here
FIGMA_FILE_ID=your_figma_file_id_here
```

- **FIGMA_TOKEN**: [Figma Settings → Personal Access Tokens](https://www.figma.com/settings/tokens),
  scoped to "File contents" (read-only).
- **FIGMA_FILE_ID**: the `{FILE_ID}` segment of `figma.com/file/{FILE_ID}/...`.

Report generation itself doesn't call the Figma API — it reads the cached
`design_tokens.json`. Credentials are only needed for `figma_cli.py` when
refreshing tokens (see [FIGMA_INTEGRATION.md](FIGMA_INTEGRATION.md)).

## 3. Usage

### Python API

```python
import json
from skills.report_generator import ReportGenerator

with open("strategy_data.json") as f:
    data = json.load(f)

gen = ReportGenerator(verbose=True)      # verbose=False to suppress logging
gen.generate_report(data, "report.html") # writes the file

html = gen.generate_report(data)         # or: get the HTML string back, no file
```

### CLI

```bash
trading-report generate --data strategy_data.json --output report.html
trading-report validate-config --verbose
trading-report --version
```

## 4. Data Format

```json
{
  "strategy": "MTF Supertrend + HARSI",
  "symbol": "BTC/USDT",
  "timeframe": "1h",
  "generated_at": "2026-07-11T10:30:00Z",
  "metrics": {
    "total_return": 2.45,
    "sharpe_ratio": 1.85,
    "max_drawdown": -0.12,
    "win_rate": 0.62,
    "profit_factor": 1.94,
    "total_trades": 42
  },
  "trades": [
    {
      "id": 1,
      "direction": "long",
      "entry_time": "2026-06-27T10:00:00Z",
      "exit_time": "2026-06-27T12:45:00Z",
      "entry_price": 62500,
      "exit_price": 63200,
      "leverage": 1,
      "bars": 3,
      "return_pct": 1.12,
      "r_multiple": 2.5,
      "pnl_usd": 700,
      "cum_pnl": 700
    }
  ]
}
```

`ReportGenerator._normalize_metrics` accepts either decimal (`0.5`) or
percentage (`50`) forms for `total_return`, `max_drawdown`, and `win_rate`,
and maps `sharpe_ratio` → `sharpe`.

## Troubleshooting

**`ModuleNotFoundError: No module named 'skills'`**
```bash
pip install -e /path/to/trading_report_generator
```

**`FIGMA_TOKEN not found` / Figma connection error**
```bash
trading-report validate-config --verbose
cat .env   # confirm FIGMA_TOKEN / FIGMA_FILE_ID are set
```

**Template not found**
- Confirm `skills/report_generator/templates/report.html.jinja2` exists in
  the installed package (reinstall with `pip install -e . --force-reinstall`
  if not).

**Design tokens not loading**
- Confirm `skills/report_generator/design_tokens.json` is valid JSON.
