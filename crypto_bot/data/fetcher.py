"""
Data Fetcher for Cryptocurrency Market Data
Fetches real-time and historical data from various exchanges
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
from typing import List, Dict, Optional
import warnings
warnings.filterwarnings('ignore')


class CryptoDataFetcher:
    """
    Fetches cryptocurrency market data from exchanges
    Supports both real-time and historical data
    """
    
    def __init__(self, exchange: str = 'binance'):
        """
        Initialize the data fetcher
        
        Args:
            exchange: Exchange name (default: binance)
        """
        self.exchange = exchange
        self.supported_exchanges = ['binance', 'coinbase', 'kraken']
        
    def fetch_ohlcv(self, symbol: str, timeframe: str = '1h', 
                     limit: int = 100) -> pd.DataFrame:
        """
        Fetch OHLCV (Open, High, Low, Close, Volume) data
        
        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            timeframe: Candle timeframe ('1m', '5m', '1h', '1d', etc.)
            limit: Number of candles to fetch
            
        Returns:
            DataFrame with OHLCV data
        """
        # Simulated data for demonstration
        # In production, integrate with ccxt or exchange APIs
        
        dates = pd.date_range(
            end=datetime.now(), 
            periods=limit, 
            freq=self._get_freq(timeframe)
        )
        
        # Generate realistic crypto price data
        base_price = 50000 if 'BTC' in symbol else 3000
        price_volatility = 0.02
        
        np.random.seed(42)
        prices = []
        current_price = base_price
        
        for i in range(limit):
            change = np.random.randn() * price_volatility * current_price
            current_price = max(current_price + change, base_price * 0.5)
            prices.append(current_price)
        
        df = pd.DataFrame({
            'timestamp': dates,
            'open': prices,
            'high': [p * (1 + np.random.uniform(0, 0.01)) for p in prices],
            'low': [p * (1 - np.random.uniform(0, 0.01)) for p in prices],
            'close': [p * (1 + np.random.uniform(-0.005, 0.005)) for p in prices],
            'volume': np.random.uniform(100, 1000, limit)
        })
        
        df['high'] = df[['open', 'close', 'high']].max(axis=1)
        df['low'] = df[['open', 'close', 'low']].min(axis=1)
        
        return df
    
    def fetch_orderbook(self, symbol: str, limit: int = 20) -> Dict:
        """
        Fetch order book data
        
        Args:
            symbol: Trading pair
            limit: Number of orders to fetch
            
        Returns:
            Dictionary with bids and asks
        """
        # Simulated order book
        base_price = 50000 if 'BTC' in symbol else 3000
        
        bids = [[base_price * (1 - i * 0.001), np.random.uniform(0.1, 2)] 
                for i in range(limit)]
        asks = [[base_price * (1 + i * 0.001), np.random.uniform(0.1, 2)] 
                for i in range(limit)]
        
        return {
            'bids': bids,
            'asks': asks,
            'timestamp': datetime.now().isoformat()
        }
    
    def fetch_ticker(self, symbol: str) -> Dict:
        """
        Fetch current ticker information
        
        Args:
            symbol: Trading pair
            
        Returns:
            Dictionary with ticker data
        """
        df = self.fetch_ohlcv(symbol, '1h', 2)
        last_row = df.iloc[-1]
        prev_row = df.iloc[-2]
        
        change = ((last_row['close'] - prev_row['close']) / prev_row['close']) * 100
        
        return {
            'symbol': symbol,
            'last': last_row['close'],
            'bid': last_row['close'] * 0.999,
            'ask': last_row['close'] * 1.001,
            'high': last_row['high'],
            'low': last_row['low'],
            'volume': last_row['volume'],
            'change_percent': change,
            'timestamp': last_row['timestamp'].isoformat()
        }
    
    def _get_freq(self, timeframe: str) -> str:
        """Convert timeframe to pandas frequency"""
        mapping = {
            '1m': '1T',
            '5m': '5T',
            '15m': '15T',
            '30m': '30T',
            '1h': '1H',
            '4h': '4H',
            '1d': '1D',
            '1w': '1W'
        }
        return mapping.get(timeframe, '1H')
    
    def add_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add technical indicators to OHLCV data
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            DataFrame with added technical indicators
        """
        df = df.copy()
        
        # Moving Averages
        df['sma_7'] = df['close'].rolling(window=7).mean()
        df['sma_25'] = df['close'].rolling(window=25).mean()
        df['sma_99'] = df['close'].rolling(window=99).mean()
        
        # Exponential Moving Average
        df['ema_12'] = df['close'].ewm(span=12).mean()
        df['ema_26'] = df['close'].ewm(span=26).mean()
        
        # MACD
        df['macd'] = df['ema_12'] - df['ema_26']
        df['macd_signal'] = df['macd'].ewm(span=9).mean()
        df['macd_hist'] = df['macd'] - df['macd_signal']
        
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        df['bb_middle'] = df['close'].rolling(window=20).mean()
        bb_std = df['close'].rolling(window=20).std()
        df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
        df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
        
        # Volume indicators
        df['volume_sma'] = df['volume'].rolling(window=20).mean()
        
        return df


if __name__ == "__main__":
    # Example usage
    fetcher = CryptoDataFetcher()
    
    # Fetch OHLCV data
    df = fetcher.fetch_ohlcv('BTC/USDT', '1h', 100)
    print("OHLCV Data:")
    print(df.head())
    
    # Add technical indicators
    df_with_indicators = fetcher.add_technical_indicators(df)
    print("\nData with Technical Indicators:")
    print(df_with_indicators.tail())
    
    # Fetch ticker
    ticker = fetcher.fetch_ticker('BTC/USDT')
    print("\nTicker:")
    print(ticker)
