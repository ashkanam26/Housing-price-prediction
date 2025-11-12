"""
Configuration management for the trading bot
"""

import json
import os
from typing import Dict, Any


class Config:
    """Configuration class for trading bot settings"""
    
    def __init__(self, config_path: str = None):
        """
        Initialize configuration
        
        Args:
            config_path: Path to configuration JSON file
        """
        self.config_path = config_path
        self.settings = self._load_default_config()
        
        if config_path and os.path.exists(config_path):
            self.load_from_file(config_path)
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration"""
        return {
            "trading": {
                "symbols": ["BTC/USDT", "ETH/USDT"],
                "timeframe": "1h",
                "initial_capital": 10000,
                "max_position_size": 0.1,  # 10% of capital
                "stop_loss_pct": 0.02,  # 2%
                "take_profit_pct": 0.05,  # 5%
            },
            "technical_analysis": {
                "indicators": ["RSI", "MACD", "BB", "SMA", "EMA"],
                "ml_model": "random_forest",
                "lookback_period": 100,
            },
            "fundamental_analysis": {
                "enabled": True,
                "factors": ["market_cap", "volume", "liquidity"],
            },
            "sentiment_analysis": {
                "enabled": True,
                "sources": ["twitter", "reddit", "news"],
                "nlp_model": "transformer",
                "sentiment_threshold": 0.6,
            },
            "news_analysis": {
                "enabled": True,
                "sources": ["cryptonews", "coindesk", "cointelegraph"],
                "update_interval": 300,  # seconds
            },
            "risk_management": {
                "max_daily_loss": 0.05,  # 5%
                "max_open_positions": 3,
                "risk_per_trade": 0.02,  # 2%
                "use_ai_risk_assessment": True,
            },
            "profit_management": {
                "trailing_stop": True,
                "trailing_stop_pct": 0.03,  # 3%
                "partial_profit_taking": True,
                "profit_levels": [0.03, 0.05, 0.08],  # 3%, 5%, 8%
            },
            "data_collection": {
                "exchange": "binance",
                "update_frequency": 60,  # seconds
                "historical_data_days": 365,
            },
            "ai_models": {
                "ml_models": ["random_forest", "xgboost", "lstm"],
                "dl_models": ["transformer", "gru"],
                "nlp_models": ["bert", "roberta"],
                "ensemble": True,
            }
        }
    
    def load_from_file(self, filepath: str):
        """Load configuration from JSON file"""
        with open(filepath, 'r') as f:
            custom_config = json.load(f)
            self.settings.update(custom_config)
    
    def save_to_file(self, filepath: str):
        """Save configuration to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.settings, f, indent=4)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        keys = key.split('.')
        value = self.settings
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value by key"""
        keys = key.split('.')
        config = self.settings
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
