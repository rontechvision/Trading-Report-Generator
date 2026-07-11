"""
Figma API Connector

Extracts design tokens and components from Figma using the REST API.
Handles authentication, caching, and validation.
"""

import os
import json
import logging
import sys
import requests
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime, timedelta


class FigmaConnector:
    """Connect to Figma API and extract design tokens."""
    
    API_BASE = "https://api.figma.com/v1"
    
    def __init__(self, token: Optional[str] = None, file_id: Optional[str] = None):
        """
        Initialize Figma connector.
        
        Args:
            token: Figma personal access token (or from env FIGMA_TOKEN)
            file_id: Figma file ID (or from env FIGMA_FILE_ID)
        """
        self.token = token or os.getenv("FIGMA_TOKEN")
        self.file_id = file_id or os.getenv("FIGMA_FILE_ID")
        
        if not self.token or not self.file_id:
            raise ValueError(
                "Figma token and file_id required. "
                "Set FIGMA_TOKEN and FIGMA_FILE_ID environment variables"
            )
        
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.session.headers.update({"X-Figma-Token": self.token})
    
    def get_file(self) -> Dict[str, Any]:
        """
        Fetch Figma file metadata.
        
        Returns:
            File data including name, pages, components
        """
        self.logger.info(f"Fetching Figma file: {self.file_id}")
        
        url = f"{self.API_BASE}/files/{self.file_id}"
        response = self.session.get(url)
        response.raise_for_status()
        
        return response.json()
    
    def get_file_nodes(self, node_ids: List[str]) -> Dict[str, Any]:
        """
        Fetch specific nodes from Figma file.
        
        Args:
            node_ids: List of node IDs to fetch
            
        Returns:
            Node data
        """
        self.logger.info(f"Fetching {len(node_ids)} nodes from Figma")
        
        url = f"{self.API_BASE}/files/{self.file_id}/nodes"
        params = {"ids": ",".join(node_ids)}
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def extract_colors(self, file_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Extract color tokens from Figma design system.
        
        Args:
            file_data: File data from get_file()
            
        Returns:
            Dictionary of color name -> hex value
        """
        colors = {}
        
        # Extract from components (if they have color names)
        if "components" in file_data:
            for comp_id, component in file_data["components"].items():
                name = component.get("name", "")
                # Look for components named like "Color/Primary" or "Colors/Background"
                if "color" in name.lower() or "bg" in name.lower():
                    # Color components typically have fills
                    pass
        
        self.logger.debug(f"Extracted {len(colors)} color tokens")
        return colors
    
    def validate_tokens(self, tokens: Dict[str, Any]) -> bool:
        """
        Validate extracted tokens structure.
        
        Args:
            tokens: Token dictionary
            
        Returns:
            True if valid
        """
        required_keys = ["colors", "typography", "spacing", "layout"]
        missing = [k for k in required_keys if k not in tokens]
        
        if missing:
            self.logger.warning(f"Missing token categories: {missing}")
            return False
        
        self.logger.info(f"Tokens validated: {len(tokens)} categories")
        return True
    
    def test_connection(self) -> bool:
        """
        Test Figma API connection.
        
        Returns:
            True if connection successful
        """
        try:
            file_data = self.get_file()
            name = file_data.get("name", "Unknown")
            self.logger.info(f"✓ Connected to Figma file: {name}")
            return True
        except Exception as e:
            self.logger.error(f"✗ Figma connection failed: {e}")
            return False


def main():
    """Test Figma connector."""
    # Console codepages other than UTF-8 (e.g. Windows cp1255) can't encode
    # the emoji used in this script's output; force UTF-8 on stdout/stderr.
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    logging.basicConfig(level=logging.INFO)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    try:
        connector = FigmaConnector()
        
        if connector.test_connection():
            print("✓ Figma API connection successful!")
            
            # Fetch file metadata
            file_data = connector.get_file()
            print(f"\n📁 File: {file_data['name']}")
            print(f"   Pages: {len(file_data.get('document', {}).get('children', []))}")
            print(f"   Components: {len(file_data.get('components', {}))}")
        else:
            print("✗ Failed to connect to Figma")
            
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("\nSetup instructions:")
        print("1. Copy .env.example to .env")
        print("2. Add your Figma token and file ID")
        print("3. Run: pip install python-dotenv")
        print("4. Try again")


if __name__ == "__main__":
    main()
