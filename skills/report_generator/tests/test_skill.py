"""Tests for report generator skill."""

import json
import pytest
from pathlib import Path
from skills.report_generator.skill import ReportGenerator


@pytest.fixture
def generator():
    """Create report generator instance."""
    return ReportGenerator()


@pytest.fixture
def sample_data():
    """Load sample data."""
    sample_path = Path(__file__).parent.parent / "sample_data.json"
    with open(sample_path) as f:
        return json.load(f)


def test_report_generator_init(generator):
    """Test that generator initializes correctly."""
    assert generator.tokens is not None
    assert "colors" in generator.tokens
    assert "typography" in generator.tokens


def test_generate_report(generator, sample_data):
    """Test report generation."""
    html = generator.generate_report(sample_data)
    
    assert html is not None
    assert len(html) > 0
    assert "<!DOCTYPE html>" in html
    assert "BTC/USDT" in html
    assert "40.7%" in html  # Check for metrics


def test_report_has_tables(generator, sample_data):
    """Test that report includes trade tables."""
    html = generator.generate_report(sample_data)
    
    assert "<table>" in html
    assert "All Trades" in html


def test_context_preparation(generator, sample_data):
    """Test context preparation for template."""
    context = generator._prepare_context(sample_data)
    
    assert context["symbol"] == "BTC/USDT"
    assert context["metrics"]["total_return_pct"] == 40.7
    assert len(context["trades"]) > 0
    assert len(context["losing_trades_sorted"]) <= 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
