"""
HTML Report Generator Skill

Generates professional financial HTML reports from strategy backtest data.
Integrates Figma design tokens for consistent styling.
"""

import json
import logging
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape


class ReportGenerator:
    """Generate HTML financial reports from strategy data."""

    def __init__(self, verbose: bool = True):
        """Initialize report generator with design tokens.
        
        Args:
            verbose: Enable logging output (default: True)
        """
        self.skill_dir = Path(__file__).parent
        self.template_dir = self.skill_dir / "templates"
        self.design_tokens_path = self.skill_dir / "design_tokens.json"
        
        # Setup logging
        level = logging.INFO if verbose else logging.WARNING
        logging.basicConfig(level=level)
        self.logger = logging.getLogger(__name__)
        self.verbose = verbose
        
        # Load design tokens from Figma (cached)
        self.logger.info(f"Loading design tokens from Figma cache: {self.design_tokens_path.name}")
        with open(self.design_tokens_path, "r") as f:
            self.tokens = json.load(f)
        
        # Validate tokens
        self.logger.info(f"✓ Design tokens loaded: {len(self.tokens)} categories")
        for category, items in self.tokens.items():
            count = len(items) if isinstance(items, dict) else 1
            self.logger.info(f"  - {category}: {count} tokens")
        
        # Setup Jinja2
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html", "xml"]),
        )
        # Inject Figma design tokens into template context
        self.env.globals.update(self.tokens)
        self.env.globals.update({
            'abs': abs,
            'format': format,
        })
        
        self.logger.info("✓ Report generator initialized with Figma design tokens")

    def generate_report(self, data: Dict[str, Any], output_path: Optional[str] = None) -> str:
        """
        Generate HTML report from strategy data.

        Args:
            data: Dictionary with strategy metrics, prices, indicators, trades
            output_path: Optional file path to save HTML. If None, returns HTML string.

        Returns:
            Generated HTML content as string.

        Example:
            >>> gen = ReportGenerator()
            >>> with open("sample_data.json") as f:
            ...     data = json.load(f)
            >>> html = gen.generate_report(data)
        """
        self.logger.info(f"Generating report for {data.get('symbol', 'Unknown')}")
        self.logger.info(f"Using Figma design tokens: {self.design_tokens_path.name}")
        
        # Prepare template context
        context = self._prepare_context(data)
        
        # Render template with Figma tokens
        self.logger.info("Rendering template with Figma design tokens...")
        template = self.env.get_template("report.html.jinja2")
        html_content = template.render(**context)
        
        self.logger.info(f"✓ Template rendered with {len(self.tokens)} token categories")
        
        # Save if output path provided
        if output_path:
            Path(output_path).write_text(html_content, encoding="utf-8")
            self.logger.info(f"✓ Report saved to {output_path}")
        
        return html_content

    def _prepare_context(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare template context from raw data.
        
        Handles multiple metric formats to support different data sources.
        """
        trades = data.get("trades", [])
        
        # Calculate cumulative P&L if not provided
        cum_pnl = 0
        for trade in trades:
            if "cum_pnl" not in trade:
                cum_pnl += trade.get("pnl_usd", 0)
                trade["cum_pnl"] = cum_pnl
        
        # Handle metrics - normalize different formats
        raw_metrics = data.get("metrics", {})
        metrics = self._normalize_metrics(raw_metrics)
        
        context = {
            "strategy": data.get("strategy_name") or data.get("strategy", "Strategy"),
            "symbol": data.get("symbol", ""),
            "timeframe": data.get("timeframe", ""),
            "period": data.get("period", ""),
            "generated_at": data.get("generated_at", str(datetime.now().date())),
            "parameters": data.get("parameters", ""),
            "metrics": metrics,
            "account": data.get("account", {}),
            "trades": trades,
            "prices": data.get("prices", {}),
            "indicators": data.get("indicators", {}),
        }
        
        # Process trades for template
        context["winning_trades"] = [t for t in context["trades"] if t.get("pnl_usd", 0) >= 0]
        context["losing_trades"] = [t for t in context["trades"] if t.get("pnl_usd", 0) < 0]
        context["losing_trades_sorted"] = sorted(
            context["losing_trades"], 
            key=lambda x: x.get("pnl_usd", 0)
        )[:10]  # Top 10 losses
        
        return context
    
    def _normalize_metrics(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize metrics to standard template format.
        
        Converts various metric formats to expected template fields:
        - total_return -> total_return_pct
        - sharpe_ratio -> sharpe
        - max_drawdown -> max_drawdown_pct
        - win_rate -> win_rate_pct (multiply by 100)
        - profit_factor (stays same)
        - total_trades (stays same)
        """
        normalized = {
            "total_return_pct": metrics.get("total_return_pct") or (metrics.get("total_return", 0) * 100),
            "sharpe": metrics.get("sharpe") or metrics.get("sharpe_ratio", 0),
            "max_drawdown_pct": metrics.get("max_drawdown_pct") or (metrics.get("max_drawdown", 0) * 100),
            "win_rate_pct": metrics.get("win_rate_pct") or (metrics.get("win_rate", 0) * 100),
            "profit_factor": metrics.get("profit_factor", 0),
            "total_trades": metrics.get("total_trades", 0),
        }
        return normalized


def main():
    """Test the report generator with sample data."""
    # Load sample data
    sample_path = Path(__file__).parent / "sample_data.json"
    with open(sample_path) as f:
        data = json.load(f)
    
    # Generate report
    gen = ReportGenerator()
    
    print("\n" + "="*60)
    print("🎨 FIGMA DESIGN TOKENS VALIDATION")
    print("="*60)
    print(f"\n✓ Design tokens loaded from: {gen.design_tokens_path}")
    print(f"✓ Token categories: {len(gen.tokens)}")
    for category, items in gen.tokens.items():
        if isinstance(items, dict):
            print(f"   • {category}: {len(items)} tokens")
        else:
            print(f"   • {category}")
    
    print("\n" + "="*60)
    print("📊 GENERATING REPORT WITH FIGMA TOKENS")
    print("="*60 + "\n")
    
    html = gen.generate_report(data)
    
    # Save output
    output_path = Path(__file__).parent / "output" / "sample_report.html"
    output_path.parent.mkdir(exist_ok=True)
    gen.generate_report(data, str(output_path))
    
    # Verify tokens are in the HTML
    print("\n" + "="*60)
    print("✅ VERIFICATION")
    print("="*60)
    
    colors = gen.tokens.get("colors", {})
    checks = {
        "background color": colors.get("background") in html,
        "surface color": colors.get("surface") in html,
        "success color": colors.get("success") in html,
        "error color": colors.get("error") in html,
        "typography": "font-family" in html,
        "spacing": "padding" in html or "margin" in html,
    }
    
    for check_name, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"{status} {check_name}")
    
    all_passed = all(checks.values())
    
    print("\n" + "="*60)
    print(f"Report: {output_path}")
    print(f"Size: {len(html):,} bytes")
    print(f"Status: {'✅ FIGMA TOKENS USED' if all_passed else '⚠️ CHECK ABOVE'}")
    print("="*60 + "\n")


if __name__ == "__main__":
    # Console codepages other than UTF-8 (e.g. Windows cp1255) can't encode
    # the emoji used in this script's output; force UTF-8 on stdout/stderr.
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    main()
