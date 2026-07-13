# Claude Professional Development Guide

## Project Overview
**Trading Report Generator** — a Python skill/package that turns strategy
backtest data (JSON) into a styled HTML report, using design tokens (colors,
typography, spacing) pulled from a Figma file.

**Scope**: This project does one thing — Figma-styled HTML report generation.

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
- [ ] Automate design token extraction from Figma component/style nodes
      (`FigmaConnector.extract_colors` is still a stub — see
      `mcp/figma_connector.py`). The current chart palette in
      `design_tokens.json` (background/up/down/grid/text/font) was pulled
      from the Figma `chart` component (node `2:8023`) via a one-off script,
      not through `extract_colors`/`figma_cli.py fetch` — those still need
      real node-walking logic before this is repeatable.
- [x] Add a chart (candlestick price + equity-curve fallback) to the report
      template, with click-a-trade-row-to-zoom/highlight. Colors are pulled
      from `design_tokens.json` (see `colors.up`/`colors.down`/`colors.grid`
      etc. in the template's `<script>` block), not hardcoded. Opens zoomed
      to the most recent 150 bars/trades (`INITIAL_BARS` in the template).
- [x] Light mode. `design_tokens.json` has a `colors_light` palette (from
      the Figma light-mode `chart` component, node `2:6654`); the template
      renders both as CSS custom properties (`:root` / `:root[data-theme]`)
      and a `COLORS_DARK`/`COLORS_LIGHT` pair for the Plotly chart, toggled
      client-side via the 🌙/☀️ button (`toggleTheme()`), no server round
      trip.
- [ ] Broaden test coverage beyond `test_skill.py`

## Token Optimization Strategy
- **Caching**: Figma design tokens are cached in `design_tokens.json` — no
  network call needed at render time.
- **Reuse**: One Jinja2 template, one token schema, shared across reports.
