"""
Command-line interface for trading-report-generator skill.

Usage:
  trading-report generate --data data.json --output report.html
  trading-report validate-config
  trading-report --version
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from skills.report_generator.skill import ReportGenerator
from skills.report_generator import __version__


def generate_command(data_file: str, output_file: Optional[str] = None, verbose: bool = False):
    """Generate HTML report from JSON data file."""
    try:
        # Load data
        data_path = Path(data_file)
        if not data_path.exists():
            print(f"❌ Error: Data file not found: {data_file}", file=sys.stderr)
            return 1
        
        with open(data_path) as f:
            data = json.load(f)
        
        # Generate report
        gen = ReportGenerator(verbose=verbose)
        html = gen.generate_report(data, output_file)
        
        if verbose:
            print(f"✓ Report generated: {len(html)} bytes")
        
        if output_file:
            print(f"✓ Saved to: {output_file}")
        else:
            print(html)
        
        return 0
    
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def validate_config_command(verbose: bool = False):
    """Validate Figma configuration."""
    try:
        from config import get_figma_connector
        
        connector = get_figma_connector()
        result = connector.test_connection()
        
        if verbose:
            print("✓ Figma connection validated successfully")
        
        return 0
    
    except Exception as e:
        print(f"❌ Configuration error: {e}", file=sys.stderr)
        if verbose:
            print("\nMake sure to set environment variables:")
            print("  FIGMA_TOKEN = Your Figma personal access token")
            print("  FIGMA_FILE_ID = Your Figma file ID")
            print("\nOr create a .env file in your project with these values.")
        
        return 1


def main():
    """Main CLI entry point."""
    # Console codepages other than UTF-8 (e.g. Windows cp1255) can't encode
    # the emoji used in this script's output; force UTF-8 on stdout/stderr.
    # Needed here (not just under __main__) since the installed
    # `trading-report` console script calls main() directly.
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Trading Report Generator - Generate professional HTML trading reports",
        prog="trading-report",
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate HTML report from data")
    generate_parser.add_argument(
        "--data",
        required=True,
        help="JSON file with strategy data and trades",
    )
    generate_parser.add_argument(
        "--output", "-o",
        help="Output HTML file (if not specified, prints to stdout)",
    )
    generate_parser.set_defaults(func=lambda args: generate_command(
        args.data, args.output, args.verbose
    ))
    
    # Validate command
    validate_parser = subparsers.add_parser("validate-config", help="Validate Figma configuration")
    validate_parser.set_defaults(func=lambda args: validate_config_command(args.verbose))
    
    args = parser.parse_args()
    
    if not hasattr(args, "func"):
        parser.print_help()
        return 0
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
