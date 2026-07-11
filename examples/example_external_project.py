#!/usr/bin/env python
"""
Example: Using trading-report-generator in a separate project

This demonstrates how to import and use the report generator
in a different project after installing the package.

Setup:
  1. pip install trading-report-generator
  2. Create .env with FIGMA_TOKEN and FIGMA_FILE_ID
  3. Run: python example_project.py
"""

import json
from pathlib import Path
from datetime import datetime

# Import the report generator from installed package
try:
    from skills.report_generator import ReportGenerator
    print("✓ Successfully imported ReportGenerator from installed package")
except ImportError as e:
    print(f"❌ Error: {e}")
    print("\nInstall package with:")
    print("  pip install -e /path/to/trading-report-generator")
    exit(1)


def create_sample_data() -> dict:
    """Create sample strategy data."""
    return {
        "strategy": "Example Strategy from External Project",
        "symbol": "ETH/USDT",
        "timeframe": "4h",
        "generated_at": datetime.now().isoformat(),
        "metrics": {
            "total_return": 3.75,
            "sharpe_ratio": 2.15,
            "max_drawdown": -0.08,
            "win_rate": 0.68,
            "profit_factor": 2.42,
            "total_trades": 28,
        },
        "trades": [
            {
                "id": 1,
                "direction": "long",
                "entry_time": "2026-07-01T08:00:00Z",
                "exit_time": "2026-07-01T16:30:00Z",
                "entry_price": 2400,
                "exit_price": 2445,
                "leverage": 1,
                "bars": 3,
                "return_pct": 1.88,
                "r_multiple": 3.2,
                "pnl_usd": 450,
                "cum_pnl": 450,
            },
            {
                "id": 2,
                "direction": "short",
                "entry_time": "2026-07-02T12:00:00Z",
                "exit_time": "2026-07-02T20:15:00Z",
                "entry_price": 2440,
                "exit_price": 2385,
                "leverage": 1,
                "bars": 2,
                "return_pct": 2.25,
                "r_multiple": 2.8,
                "pnl_usd": 550,
                "cum_pnl": 1000,
            },
        ],
    }


def main():
    """Main example showing package usage."""
    print("\n" + "="*60)
    print("EXAMPLE: Using trading-report-generator in external project")
    print("="*60 + "\n")
    
    # Initialize report generator
    print("1️⃣  Initializing report generator...")
    gen = ReportGenerator(verbose=True)
    print(f"   ✓ Loaded {len(gen.tokens)} token categories\n")
    
    # Create sample data
    print("2️⃣  Creating sample strategy data...")
    data = create_sample_data()
    print(f"   ✓ Strategy: {data['strategy']}")
    print(f"   ✓ Trades: {len(data['trades'])}\n")
    
    # Generate report
    print("3️⃣  Generating HTML report...")
    output_path = Path("external_project_report.html")
    html = gen.generate_report(data, str(output_path))
    print(f"   ✓ Generated {len(html):,} bytes\n")
    
    # Verify output
    print("4️⃣  Verifying report...")
    if output_path.exists():
        file_size = output_path.stat().st_size
        print(f"   ✓ File saved: {output_path}")
        print(f"   ✓ File size: {file_size:,} bytes")
        print(f"\n✓ Success! Open {output_path} in your browser\n")
    else:
        print(f"   ❌ File not created: {output_path}\n")
    
    print("="*60)
    print("Example usage patterns:")
    print("="*60)
    
    print("\n📝 Pattern 1: Simple generation")
    print("""
    from skills.report_generator import ReportGenerator
    
    gen = ReportGenerator()
    gen.generate_report(data, "report.html")
    """)
    
    print("\n📝 Pattern 2: Get HTML string (no file)")
    print("""
    gen = ReportGenerator()
    html = gen.generate_report(data)  # Returns HTML string
    """)
    
    print("\n📝 Pattern 3: Silent mode (no logging)")
    print("""
    gen = ReportGenerator(verbose=False)
    gen.generate_report(data, "report.html")
    """)
    
    print("\n📝 Pattern 4: CLI usage")
    print("""
    trading-report generate --data data.json --output report.html
    """)
    
    print("\n💡 For more usage patterns, see INSTALLATION.md")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
