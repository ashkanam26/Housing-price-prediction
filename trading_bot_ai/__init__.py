"""
AI-Powered Cryptocurrency Trading Bot
======================================

A comprehensive trading bot with:
- Technical Analysis (ML-based indicators)
- Fundamental Analysis
- Sentiment Analysis (NLP)
- News Analysis (NLP)
- Risk Management (AI-based)
- Profit Management
"""

__version__ = "1.0.0"
__author__ = "Trading Bot AI Team"

from .trading_bot import TradingBot
from .config import Config

__all__ = ['TradingBot', 'Config']
