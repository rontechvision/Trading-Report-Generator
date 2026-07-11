"""
Setup and Configuration Helper

Handles environment setup, token validation, and Figma integration.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv, find_dotenv


def setup_environment():
    """
    Load and validate environment configuration.
    
    Returns:
        True if setup successful
    """
    # Find and load .env file
    env_path = find_dotenv()
    
    if not env_path:
        print("⚠ No .env file found")
        print("\nTo use Figma integration:")
        print("  1. Copy .env.example to .env")
        print("     cp .env.example .env")
        print("  2. Edit .env and add your Figma token")
        print("  3. Run setup again")
        return False
    
    load_dotenv(env_path)
    
    # Check required tokens
    figma_token = os.getenv("FIGMA_TOKEN")
    figma_file = os.getenv("FIGMA_FILE_ID")
    
    status = True
    
    print("✓ Environment Configuration:")
    if figma_token and figma_token != "your_personal_access_token_here":
        print(f"  ✓ FIGMA_TOKEN: {figma_token[:10]}...{figma_token[-4:]}")
    else:
        print("  ✗ FIGMA_TOKEN: Not configured")
        status = False
    
    if figma_file:
        print(f"  ✓ FIGMA_FILE_ID: {figma_file}")
    else:
        print("  ✗ FIGMA_FILE_ID: Not configured")
        status = False
    
    return status


def get_figma_connector():
    """
    Get Figma connector instance with validated config.
    
    Returns:
        FigmaConnector or None if config invalid
    """
    from mcp.figma_connector import FigmaConnector
    
    if not setup_environment():
        return None
    
    try:
        connector = FigmaConnector()
        return connector
    except Exception as e:
        print(f"✗ Failed to initialize Figma connector: {e}")
        return None


if __name__ == "__main__":
    # Console codepages other than UTF-8 (e.g. Windows cp1255) can't encode
    # the checkmarks/emoji used in this script's output; force UTF-8.
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    setup_environment()
