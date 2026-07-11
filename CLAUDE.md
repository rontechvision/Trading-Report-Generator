# Claude Professional Development Guide

## Project Overview
**Trading Report Generator** — a Python skill/package that turns strategy
backtest data (JSON) into a styled HTML report, using design tokens (colors,
typography, spacing) pulled from a Figma file.

**Scope**: This project does one thing — Figma-styled HTML report generation.
It is not a trading bot, MCP orchestration platform, or alerting system.
Telegram, auto-trading, strategy analysis, and backtesting belong in other
projects (e.g. `TradingBotClaude`), not here.

**Tech Stack**: Python, Jinja2, Figma REST API

---

## Architecture

```
Figma file (design system)
       ↓  Figma REST API
FigmaConnector (mcp/figma_connector.py)
       ↓
TokensValidator (skills/report_generator/figma_tokens_extractor.py)
       ↓
design_tokens.json (cached locally — no API call needed to render)
       ↓
ReportGenerator (skills/report_generator/skill.py) + report.html.jinja2
       ↓
Rendered HTML trading report
```

See [FIGMA_INTEGRATION.md](FIGMA_INTEGRATION.md) for the Figma-side details.

## File Structure
```
trading_report_generator/
├── CLAUDE.md                 # This file
├── .instructions.md          # Claude Code development guidelines
├── README.md                 # Overview & quick start
├── INSTALLATION.md           # Install, setup, usage examples, data format
├── FIGMA_INTEGRATION.md      # Figma token extraction details
├── config.py                 # .env loading + FigmaConnector factory
├── figma_cli.py              # CLI: validate / test-connection / fetch / setup
├── setup.py                  # Package config (pip install -e .)
├── requirements.txt
├── mcp/
│   └── figma_connector.py    # Figma REST API client
├── skills/
│   └── report_generator/
│       ├── skill.py                   # ReportGenerator (core logic)
│       ├── cli.py                     # `trading-report` CLI
│       ├── figma_tokens_extractor.py  # Token validation
│       ├── design_tokens.json         # Cached Figma design tokens
│       ├── sample_data.json           # Test data
│       ├── templates/report.html.jinja2
│       ├── tests/test_skill.py
│       └── output/                    # Generated reports (gitignored)
└── examples/
    └── example_external_project.py    # Usage from another project
```

---

## Status
Core skill is functional: loads cached Figma tokens, renders a strategy's
metrics/trades into a styled HTML report, and exposes both a Python API
(`ReportGenerator`) and a CLI (`trading-report`).

## Remaining Work
- [ ] Extract design tokens directly from Figma component/style nodes
      (`FigmaConnector.extract_colors` is currently a stub — see
      `mcp/figma_connector.py`)
- [ ] Add a chart (equity curve / price) to the report template
- [ ] Broaden test coverage beyond `test_skill.py`

## Token Optimization Strategy
- **Caching**: Figma design tokens are cached in `design_tokens.json` — no
  network call needed at render time.
- **Reuse**: One Jinja2 template, one token schema, shared across reports.
