# Figma Integration Guide

## Overview

Your project now has automated **Figma Design Token extraction** integrated. This ensures your HTML reports always use the design system colors, typography, and spacing from Figma.

## Architecture

```
Figma Design File
       ↓
   API (v1/REST)
       ↓
FigmaConnector (mcp/figma_connector.py)
       ↓
TokensValidator (skills/report_generator/figma_tokens_extractor.py)
       ↓
design_tokens.json (cached locally)
       ↓
report.html.jinja2 (uses tokens in CSS)
```

## Setup (Already Complete ✅)

### 1. Environment Configuration
- ✅ Created `.env.example` (template)
- ✅ Created `.env` (with your credentials)
- ✅ Added to `.gitignore` (safe, won't commit)

### 2. Figma Credentials
```
FIGMA_TOKEN: figd_Nwcum...yUFT (your personal token)
FIGMA_FILE_ID: 6eCCUGFL617dFcuxuAKlG8 (Free Financial Components — Light/Dark, community copy)
```

### 3. Files Created
| File | Purpose |
|------|---------|
| `mcp/figma_connector.py` | Figma API client |
| `skills/report_generator/figma_tokens_extractor.py` | Token validation & extraction |
| `figma_cli.py` | CLI tool for token management |
| `config.py` | Environment setup helper |
| `.env` | Your credentials (⚠️ Never commit) |
| `.env.example` | Template for others |
| `.gitignore` | Excludes `.env` from git |

## Usage

### Test Figma Connection
```bash
python figma_cli.py test-connection
```
Output:
```
✓ Connected to Figma file: Free Financial Components Light & Dark (Community)
```

### Validate Current Tokens
```bash
python figma_cli.py validate
```
Output:
```
📋 Design Tokens Validation Report:
   Valid: ✓ Yes
   Categories: 4 (colors, typography, spacing, layout)
   Colors: 13
   Typography: 6
   Spacing: 6
```

### Fetch Fresh Tokens from Figma
```bash
python figma_cli.py fetch
```
This will:
1. Connect to Figma API
2. Fetch file metadata
3. Validate token structure
4. Update `design_tokens.json` if needed

### Setup New Installation
```bash
python figma_cli.py setup
```
Guides new users through configuration.

## Current Design Tokens

### Colors (15 tokens)
- Primary: background (`#181b21`), surface (`#2a2d34`), border (`#57595f`)
- Text: primary, secondary, tertiary
- Status: success, error
- Trading: long (buy), short (sell)
- Chart: up (`#366aef`) / down (`#f1364e`) candle colors, grid
  (`rgba(255,255,255,0.08)`) — pulled from the Figma `chart` component
  (node `2:8023`) in the file above
- Highlight, accent

### Typography (6 definitions)
- heading_1: 21px, weight 700
- heading_2: 15px, weight 700
- body: 13px, weight 400
- small: 11px, weight 400
- tiny: 10px, weight 400
- font-family: `'Plus Jakarta Display', ...` (from the Figma chart's text
  nodes, falls back to system fonts)

### Spacing (6 values)
- xs: 2px, sm: 6px, md: 10px
- lg: 14px, xl: 18px, xxl: 24px

### Layout
- max_width: 1240px
- border_radius: 8px
- card_padding: 8px 12px

## Integration Points

### In Report Generation
```python
# In skill.py
from mcp.figma_connector import FigmaConnector
from skills.report_generator.figma_tokens_extractor import TokensValidator

# Tokens automatically loaded from design_tokens.json
self.env.globals.update(self.tokens)
```

### In HTML Template
```html
<!-- Uses CSS variables from design_tokens.json -->
<style>
  body { 
    background: {{ colors.background }};
    color: {{ colors.text_primary }};
    font-family: {{ typography.font_family }};
  }
  .card {
    padding: {{ spacing.md }};
    border-radius: {{ layout.border_radius }};
  }
</style>
```

## Advanced Usage

### Extract Specific Figma Components
`FigmaConnector.extract_colors` is still a stub — it scans component names
but never reads their fills. To pull real colors today, fetch the node
directly and read `fills`/`strokes` off each child (this is how the chart
palette in `design_tokens.json` was populated, from node `2:8023`):

```python
from mcp.figma_connector import FigmaConnector

connector = FigmaConnector()
node_data = connector.get_file_nodes(["2:8023"])  # node id from the Figma URL

# walk node_data["nodes"]["2:8023"]["document"]["children"], reading
# node["fills"][i]["color"] (SOLID fills) for each named element
```

Making `extract_colors` do this walk generically (and running it through
`figma_cli.py fetch`) is still open — see CLAUDE.md's Remaining Work.

### Custom Token Extraction
Extend `TokensValidator` to extract from:
- Figma color styles
- Figma text styles
- Figma component properties

### Automation (Future)
```bash
# Could add to CI/CD to auto-update tokens daily
# 0 0 * * * python figma_cli.py fetch > /var/log/tokens-update.log 2>&1
```

## Troubleshooting

### "No .env file found"
```bash
# Copy template to .env
cp .env.example .env
# Edit and add your credentials
```

### "Figma token invalid"
1. Visit: https://www.figma.com/settings/tokens
2. Generate new personal access token
3. Update in `.env`
4. Test: `python figma_cli.py test-connection`

### "Tokens validation failed"
```bash
# Check what's missing
python figma_cli.py validate

# Restore from backup or regenerate
cp design_tokens.json design_tokens.json.bak
```

## File Structure
```
MyWebSkill/
├── .env                    # Your credentials (⚠️ secret)
├── .env.example           # Template for others
├── figma_cli.py          # CLI tool
├── config.py             # Environment helper
├── requirements.txt      # python-dotenv added
│
├── mcp/
│   └── figma_connector.py        # Figma API client
│
└── skills/report_generator/
    ├── figma_tokens_extractor.py # Token validation
    ├── design_tokens.json        # Cached tokens
    └── templates/
        └── report.html.jinja2    # Uses tokens
```

## Next Steps

1. ✅ Figma API integrated
2. ✅ Design tokens validated
3. → Enhance token extraction (extract from Figma components)
4. → Auto-update tokens on report generation
5. → Version control for tokens (git-based)

## Security Notes

- ✅ `.env` excluded from git (in `.gitignore`)
- ✅ Token only exists locally
- ✅ Never commit credentials
- ⚠️ If token is exposed, regenerate immediately at https://www.figma.com/settings/tokens

## Commands Quick Reference

```bash
# Setup
python figma_cli.py setup              # First-time configuration

# Testing
python figma_cli.py test-connection    # Verify API access

# Tokens
python figma_cli.py validate           # Check current tokens
python figma_cli.py fetch              # Update from Figma

# Generate Report (automatically uses tokens)
python -m skills.report_generator.skill
```

---

**Status**: Figma integration complete ✅ (manual node extraction; automated
`extract_colors` still a stub)  
**Connected to**: Free Financial Components — Light/Dark (community copy)  
**Tokens Validated**: ✓ Yes  
**Last Check**: 2026-07-13
