#!/usr/bin/env python
"""
Design Tokens CLI

Manage Figma design token extraction and validation.

Usage:
    python figma_cli.py validate      - Validate current tokens
    python figma_cli.py test-connection - Test Figma API connection  
    python figma_cli.py fetch         - Fetch fresh tokens from Figma (requires .env)
    python figma_cli.py setup         - Setup environment configuration
"""

import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))


def setup_logging():
    """Configure logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s'
    )


def cmd_validate():
    """Validate current design tokens."""
    from skills.report_generator.figma_tokens_extractor import validate_current_tokens
    
    tokens_path = Path(__file__).parent / "skills" / "report_generator" / "design_tokens.json"
    validate_current_tokens(tokens_path)


def cmd_test_connection():
    """Test Figma API connection."""
    from config import get_figma_connector
    
    print("🔗 Testing Figma API Connection...\n")
    
    connector = get_figma_connector()
    if connector:
        connector.test_connection()
    else:
        print("✗ Failed to initialize connector")


def cmd_fetch():
    """Fetch fresh tokens from Figma."""
    from config import get_figma_connector
    from skills.report_generator.figma_tokens_extractor import TokensValidator
    
    print("📥 Fetching Figma Design Tokens...\n")
    
    connector = get_figma_connector()
    if not connector:
        print("✗ Cannot fetch without valid Figma configuration")
        return
    
    try:
        # Fetch file data
        print("1. Fetching Figma file metadata...")
        file_data = connector.get_file()
        print(f"   ✓ File: {file_data['name']}")
        
        # For now, validate existing tokens as proof of concept
        # Full token extraction would parse components/styles from the file
        print("\n2. Validating token structure...")
        validator = TokensValidator(
            Path(__file__).parent / "skills" / "report_generator" / "design_tokens.json"
        )
        
        # Load current tokens
        tokens = validator.load_tokens()
        
        if validator.validate_structure(tokens):
            print("   ✓ Current tokens are valid")
            print("\n✓ Token fetch complete!")
            print("\nNote: Full token extraction from components requires parsing")
            print("Figma's component tree. Current implementation validates existing tokens.")
        else:
            print("   ✗ Token structure issues found")
            
    except Exception as e:
        print(f"✗ Error during fetch: {e}")
        import traceback
        traceback.print_exc()


def cmd_setup():
    """Setup environment configuration."""
    from config import setup_environment
    
    print("⚙️  Setting up Figma Integration...\n")
    
    env_file = Path(".env")
    example_file = Path(".env.example")
    
    if not env_file.exists() and example_file.exists():
        print("📋 Found .env.example")
        print("\nTo get started:")
        print("1. Copy .env.example to .env:")
        print("   cp .env.example .env")
        print("\n2. Get your Figma token from:")
        print("   https://www.figma.com/settings/tokens")
        print("\n3. Edit .env and add:")
        print("   FIGMA_TOKEN=your_token_here")
        print("   FIGMA_FILE_ID=5qTgjz00GA5tSNaV9nKCqM")
        print("\n4. Test connection:")
        print("   python figma_cli.py test-connection")
    elif env_file.exists():
        print("✓ .env file exists")
        setup_environment()
    else:
        print("✗ No .env or .env.example found")


def main():
    """Main CLI entry point."""
    # Console codepages other than UTF-8 (e.g. Windows cp1255) can't encode
    # the emoji used in this script's output; force UTF-8 on stdout/stderr.
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    setup_logging()
    
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1].lower()
    
    commands = {
        "validate": cmd_validate,
        "test-connection": cmd_test_connection,
        "fetch": cmd_fetch,
        "setup": cmd_setup,
    }
    
    if command in commands:
        try:
            commands[command]()
        except Exception as e:
            print(f"✗ Command failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    else:
        print(f"✗ Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
