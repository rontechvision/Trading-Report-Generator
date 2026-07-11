# trading-report-generator

A Python skill that turns strategy backtest data (JSON) into a professional
HTML trading report, styled with design tokens (colors, typography, spacing)
cached from a Figma file.

This project does one thing: **Figma-styled HTML report generation.** No
Telegram, no auto-trading, no data connectors.

## Quick Start

1. **Install the package**

   From a local clone:
   ```bash
   pip install -e /path/to/trading_report_generator
   ```

   Or straight from GitHub — globally (via `pipx`) or into a specific
   project's virtualenv (via `pip`):
   ```bash
   # Global CLI, available in every shell
   pipx install git+https://github.com/rontechvision/Trading-Report-Generator.git

   # Project-specific, inside that project's venv
   pip install git+https://github.com/rontechvision/Trading-Report-Generator.git
   ```
   **See [INSTALLATION.md](INSTALLATION.md#1-install-the-package)** for the
   full breakdown of global vs. project-specific installs, version pinning,
   and upgrading.

2. **Create `.env` with your Figma credentials**
   ```bash
   FIGMA_TOKEN=your_personal_access_token
   FIGMA_FILE_ID=your_file_id
   ```

3. **Generate a report in Python**
   ```python
   import json
   from skills.report_generator import ReportGenerator

   with open("strategy_data.json") as f:
       data = json.load(f)

   gen = ReportGenerator()
   gen.generate_report(data, "report.html")
   ```

4. **...or use the CLI**
   ```bash
   trading-report generate --data strategy_data.json --output report.html
   ```

**See [INSTALLATION.md](INSTALLATION.md)** for the data format, CLI reference,
and troubleshooting.
**See [FIGMA_INTEGRATION.md](FIGMA_INTEGRATION.md)** for how Figma tokens are
fetched, cached, and wired into the template.

## Project Structure

```
trading_report_generator/
├── CLAUDE.md                # Project scope & architecture
├── INSTALLATION.md           # Setup, usage, data format, troubleshooting
├── FIGMA_INTEGRATION.md      # Figma token pipeline
├── config.py                 # .env loading + FigmaConnector factory
├── figma_cli.py               # CLI: validate / test-connection / fetch / setup
├── setup.py                  # Package config
├── requirements.txt
│
├── skills/
│   └── report_generator/     # The skill
│       ├── skill.py                   # ReportGenerator
│       ├── cli.py                     # `trading-report` CLI
│       ├── figma_tokens_extractor.py  # Token validation
│       ├── design_tokens.json         # Cached Figma design system
│       ├── sample_data.json           # Test data
│       ├── templates/report.html.jinja2
│       ├── tests/test_skill.py
│       └── output/                    # Generated reports (gitignored)
│
├── mcp/
│   └── figma_connector.py    # Figma REST API client
│
└── examples/
    └── example_external_project.py  # Usage from another project
```

## Local Development

```bash
pip install -r requirements.txt
python -m skills.report_generator.skill
```

This loads `sample_data.json`, renders it with the cached Figma tokens, and
writes `skills/report_generator/output/sample_report.html` — open it in a
browser to see the result.

## Customization

- Edit `skills/report_generator/design_tokens.json` to change colors,
  typography, or spacing (or refetch from Figma — see FIGMA_INTEGRATION.md).
- Edit `skills/report_generator/templates/report.html.jinja2` to change the
  report layout.

---

**Status**: Core skill functional — see [CLAUDE.md](CLAUDE.md) for what's left.
