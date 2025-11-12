"""
Market Data Collection Module
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class MarketDataCollector:
    """Collect and manage cryptocurrency market data"""
    
    def __init__(self, config: Dict):
        """
        Initialize market data collector
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.data_config = config.get('data_collection', {})
        self.exchange = self.data_config.get('exchange', 'binance')
        self.update_frequency = self.data_config.get('update_frequency', 60)
        
        # Cache for market data
        self.cache = {}
        self.last_update = {}
    
    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str = '1h',
        limit: int = 100
    ) -> pd.DataFrame:
        """
        Fetch OHLCV (Open, High, Low, Close, Volume) data
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTC/USDT')
            timeframe: Timeframe (e.g., '1m', '5m', '1h', '1d')
            limit: Number of candles to fetch
            
        Returns:
            DataFrame with OHLCV data
        """
        # Check cache
        cache_key = f"{symbol}_{timeframe}"
        if cache_key in self.cache:
            last_update = self.last_update.get(cache_key)
            if last_update and (datetime.now() - last_update).seconds < self.update_frequency:
                return self.cache[cache_key]
        
        # Simulate fetching data (in real implementation, use exchange API)
        df = self._simulate_ohlcv_data(symbol, timeframe, limit)
        
        # Update cache
        self.cache[cache_key] = df
        self.last_update[cache_key] = datetime.now()
        
        return df
    
    def _simulate_ohlcv_data(
        self,
        symbol: str,
        timeframe: str,
        limit: int
    ) -> pd.DataFrame:
        """
        Simulate OHLCV data for demonstration
        In production, this would fetch real data from exchange API
        """
        # Generate timestamps
        now = datetime.now()
        timeframe_minutes = self._get_timeframe_minutes(timeframe)
        timestamps = [now - timedelta(minutes=timeframe_minutes * i) for i in range(limit, 0, -1)]
        
        # Generate simulated price data (random walk)
        base_price = 50000 if 'BTC' in symbol else 3000 if 'ETH' in symbol else 100
        returns = np.random.randn(limit) * 0.02  # 2% volatility
        prices = base_price * np.exp(np.cumsum(returns))
        
        # Generate OHLCV
        data = []
        for i, (ts, close) in enumerate(zip(timestamps, prices)):
            high = close * (1 + abs(np.random.randn()) * 0.01)
            low = close * (1 - abs(np.random.randn()) * 0.01)
            open_price = prices[i-1] if i > 0 else close
            volume = np.random.uniform(100, 1000) * base_price / 100
            
            data.append({
                'timestamp': ts,
                'open': open_price,
                'high': high,
                'low': low,
                'close': close,
                'volume': volume
            })
        
        df = pd.DataFrame(data)
        df.set_index('timestamp', inplace=True)
        return df
    
    def _get_timeframe_minutes(self, timeframe: str) -> int:
        """Convert timeframe string to minutes"""
        mapping = {
            '1m': 1, '5m': 5, '15m': 15, '30m': 30,
            '1h': 60, '4h': 240, '1d': 1440, '1w': 10080
        }
        return mapping.get(timeframe, 60)
    
    def fetch_ticker(self, symbol: str) -> Dict[str, any]:
        """
        Fetch current ticker data
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            Ticker data dictionary
        """
        # Simulate ticker data
        df = self.fetch_ohlcv(symbol, '1m', 1)
        if len(df) == 0:
            return {}
        
        last_row = df.iloc[-1]
        return {
            'symbol': symbol,
            'last_price': last_row['close'],
            'bid': last_row['close'] * 0.999,
            'ask': last_row['close'] * 1.001,
            'volume_24h': last_row['volume'] * 1440,  # Approximate daily volume
            'high_24h': last_row['high'] * 1.02,
            'low_24h': last_row['low'] * 0.98,
            'price_change_24h': np.random.uniform(-5, 5),
            'timestamp': datetime.now()
        }
    
    def fetch_order_book(self, symbol: str, depth: int = 20) -> Dict[str, List]:
        """
        Fetch order book data
        
        Args:
            symbol: Trading pair symbol
            depth: Order book depth
            
        Returns:
            Order book with bids and asks
        """
        ticker = self.fetch_ticker(symbol)
        mid_price = ticker.get('last_price', 100)
        
        # Simulate order book
        bids = []
        asks = []
        
        for i in range(depth):
            bid_price = mid_price * (1 - (i + 1) * 0.0001)
            ask_price = mid_price * (1 + (i + 1) * 0.0001)
            
            bids.append([bid_price, np.random.uniform(0.1, 2.0)])
            asks.append([ask_price, np.random.uniform(0.1, 2.0)])
        
        return {
            'symbol': symbol,
            'bids': bids,
            'asks': asks,
            'timestamp': datetime.now()
        }
    
    def fetch_fundamental_data(self, symbol: str) -> Dict[str, any]:
        """
        Fetch fundamental data for cryptocurrency
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            Fundamental data dictionary
        """
        base_asset = symbol.split('/')[0]
        
        # Simulate fundamental data
        if base_asset == 'BTC':
            market_cap = np.random.uniform(800e9, 1000e9)
            dominance = np.random.uniform(40, 50)
        elif base_asset == 'ETH':
            market_cap = np.random.uniform(300e9, 400e9)
            dominance = np.random.uniform(15, 20)
        else:
            market_cap = np.random.uniform(1e9, 10e9)
            dominance = np.random.uniform(0.1, 2)
        
        ticker = self.fetch_ticker(symbol)
        
        return {
            'symbol': symbol,
            'market_cap': market_cap,
            'volume_24h': ticker.get('volume_24h', 0),
            'avg_volume': ticker.get('volume_24h', 0) * np.random.uniform(0.8, 1.2),
            'price_change_24h': ticker.get('price_change_24h', 0),
            'price_change_7d': np.random.uniform(-15, 15),
            'price_change_30d': np.random.uniform(-30, 30),
            'market_dominance': dominance,
            'liquidity_score': np.random.uniform(0.5, 1.0),
            'volatility_30d': np.random.uniform(0.2, 0.6),
            'circulating_supply': market_cap / ticker.get('last_price', 1),
            'max_supply': None if base_asset in ['ETH'] else market_cap / ticker.get('last_price', 1) * 1.1
        }
    
    def get_historical_data(
        self,
        symbol: str,
        days: int = 365
    ) -> pd.DataFrame:
        """
        Get historical data for specified period
        
        Args:
            symbol: Trading pair symbol
            days: Number of days of history
            
        Returns:
            DataFrame with historical data
        """
        # For demonstration, fetch daily data
        return self.fetch_ohlcv(symbol, '1d', days)
    
    def calculate_volatility(self, df: pd.DataFrame, period: int = 30) -> float:
        """Calculate price volatility"""
        if len(df) < period:
            return 0.0
        
        returns = df['close'].pct_change().dropna()
        volatility = returns.tail(period).std() * np.sqrt(365)  # Annualized
        return volatility
    
    def get_support_resistance(self, df: pd.DataFrame) -> Dict[str, List[float]]:
        """
        Identify support and resistance levels
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            Dictionary with support and resistance levels
        """
        if len(df) < 20:
            return {'support': [], 'resistance': []}
        
        # Simple pivot point method
        highs = df['high'].values
        lows = df['low'].values
        closes = df['close'].values
        
        # Find local maxima and minima
        resistance_levels = []
        support_levels = []
        
        window = 10
        for i in range(window, len(df) - window):
            # Check for local maximum (resistance)
            if highs[i] == max(highs[i-window:i+window+1]):
                resistance_levels.append(highs[i])
            
            # Check for local minimum (support)
            if lows[i] == min(lows[i-window:i+window+1]):
                support_levels.append(lows[i])
        
        # Get unique levels and sort
        resistance_levels = sorted(set(resistance_levels), reverse=True)[:3]
        support_levels = sorted(set(support_levels))[:3]
        
        return {
            'resistance': resistance_levels,
            'support': support_levels
        }
    
    def get_market_summary(self, symbols: List[str]) -> List[Dict]:
        """
        Get market summary for multiple symbols
        
        Args:
            symbols: List of trading pair symbols
            
        Returns:
            List of market summaries
        """
        summaries = []
        
        for symbol in symbols:
            ticker = self.fetch_ticker(symbol)
            fundamental = self.fetch_fundamental_data(symbol)
            
            summaries.append({
                'symbol': symbol,
                'price': ticker.get('last_price'),
                'change_24h': ticker.get('price_change_24h'),
                'volume_24h': ticker.get('volume_24h'),
                'market_cap': fundamental.get('market_cap'),
                'timestamp': datetime.now()
            })
        
        return summaries
