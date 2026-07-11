"""
trading-report-generator: Professional HTML trading reports with Figma design tokens

Quick Start:
  from skills.report_generator import ReportGenerator
  
  gen = ReportGenerator()
  html = gen.generate_report(data)
"""

__version__ = "0.1.0"
__author__ = "Trading Bot Claude"
__license__ = "MIT"

from skills.report_generator.skill import ReportGenerator

__all__ = ["ReportGenerator"]
