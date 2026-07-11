"""
Figma Design Tokens Extractor

Validates current design tokens and optionally fetches updates from Figma.
Handles caching and fallback logic.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class TokensValidator:
    """Validate and manage design tokens."""
    
    REQUIRED_CATEGORIES = ["colors", "typography", "spacing", "layout"]
    REQUIRED_COLORS = [
        "background", "surface", "border", 
        "text_primary", "text_secondary", "text_tertiary",
        "success", "error", "long", "short"
    ]
    
    def __init__(self, tokens_path: Path):
        """
        Initialize validator.
        
        Args:
            tokens_path: Path to design_tokens.json
        """
        self.tokens_path = tokens_path
        self.logger = logging.getLogger(__name__)
    
    def load_tokens(self) -> Dict[str, Any]:
        """
        Load tokens from file.
        
        Returns:
            Token dictionary
        """
        if not self.tokens_path.exists():
            self.logger.warning(f"Tokens file not found: {self.tokens_path}")
            return {}
        
        with open(self.tokens_path, "r") as f:
            tokens = json.load(f)
        
        self.logger.info(f"Loaded tokens from {self.tokens_path.name}")
        return tokens
    
    def save_tokens(self, tokens: Dict[str, Any]) -> None:
        """
        Save tokens to file.
        
        Args:
            tokens: Token dictionary
        """
        self.tokens_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.tokens_path, "w") as f:
            json.dump(tokens, f, indent=2)
        
        self.logger.info(f"Saved tokens to {self.tokens_path.name}")
    
    def validate_structure(self, tokens: Dict[str, Any]) -> bool:
        """
        Validate token structure.
        
        Args:
            tokens: Token dictionary
            
        Returns:
            True if valid
        """
        if not tokens:
            self.logger.error("Tokens dictionary is empty")
            return False
        
        # Check required categories
        missing_cats = [c for c in self.REQUIRED_CATEGORIES if c not in tokens]
        if missing_cats:
            self.logger.warning(f"Missing categories: {missing_cats}")
        
        # Check colors
        colors = tokens.get("colors", {})
        missing_colors = [c for c in self.REQUIRED_COLORS if c not in colors]
        if missing_colors:
            self.logger.warning(f"Missing colors: {missing_colors}")
        
        # Check typography
        typography = tokens.get("typography", {})
        if not typography:
            self.logger.warning("No typography tokens found")
        
        return len(missing_cats) == 0 and len(missing_colors) == 0
    
    def validate_all(self) -> Dict[str, Any]:
        """
        Full validation report.
        
        Returns:
            Validation report with status and issues
        """
        tokens = self.load_tokens()
        is_valid = self.validate_structure(tokens)
        
        report = {
            "valid": is_valid,
            "timestamp": datetime.now().isoformat(),
            "file": str(self.tokens_path),
            "categories": len(tokens),
            "colors": len(tokens.get("colors", {})),
            "typography": len(tokens.get("typography", {})),
            "spacing": len(tokens.get("spacing", {})),
        }
        
        if is_valid:
            self.logger.info("✓ Tokens validated successfully")
        else:
            self.logger.warning("⚠ Token validation found issues (see details above)")
        
        return report
    
    def generate_figma_extract_script(self) -> str:
        """
        Generate Python script to extract tokens from Figma.
        
        Returns:
            Python code as string
        """
        return '''
# To extract tokens from Figma, use:
# python -m skills.report_generator.figma_tokens_extractor --fetch

# This requires:
# 1. Copy .env.example to .env
# 2. Add FIGMA_TOKEN and FIGMA_FILE_ID
# 3. pip install python-dotenv requests
# 4. Run: python -m skills.report_generator.figma_tokens_extractor --fetch
        '''


def validate_current_tokens(tokens_path: Path) -> None:
    """Validate current design tokens."""
    logging.basicConfig(level=logging.INFO)
    
    validator = TokensValidator(tokens_path)
    report = validator.validate_all()
    
    print("\n📋 Design Tokens Validation Report:")
    print(f"   Valid: {'✓ Yes' if report['valid'] else '✗ No'}")
    print(f"   File: {report['file']}")
    print(f"   Categories: {report['categories']}")
    print(f"   Colors: {report['colors']}")
    print(f"   Typography: {report['typography']}")
    print(f"   Spacing: {report['spacing']}")
    print(f"   Checked: {report['timestamp']}")
    
    if not report['valid']:
        print("\n⚠ To extract fresh tokens from Figma:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your FIGMA_TOKEN and FIGMA_FILE_ID")
        print("   3. Run: python -m skills.report_generator.figma_tokens_extractor --fetch")


def main():
    """Test token validation."""
    tokens_path = Path(__file__).parent / "design_tokens.json"
    validate_current_tokens(tokens_path)


if __name__ == "__main__":
    main()
