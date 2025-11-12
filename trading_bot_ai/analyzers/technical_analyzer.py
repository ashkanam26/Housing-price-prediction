"""
Technical Analysis Module with ML-based indicators
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')


class TechnicalAnalyzer:
    """Technical analysis with ML-based pattern recognition"""
    
    def __init__(self, config: Dict):
        """
        Initialize technical analyzer
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.scaler = StandardScaler()
        self.ml_model = None
        self._initialize_ml_model()
    
    def _initialize_ml_model(self):
        """Initialize ML model for pattern recognition"""
        model_type = self.config.get('technical_analysis', {}).get('ml_model', 'random_forest')
        
        if model_type == 'random_forest':
            self.ml_model = RandomForestClassifier(n_estimators=100, random_state=42)
        elif model_type == 'gradient_boosting':
            self.ml_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
        else:
            self.ml_model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate technical indicators
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            DataFrame with calculated indicators
        """
        df = df.copy()
        
        # Moving Averages
        df['SMA_20'] = df['close'].rolling(window=20).mean()
        df['SMA_50'] = df['close'].rolling(window=50).mean()
        df['EMA_12'] = df['close'].ewm(span=12, adjust=False).mean()
        df['EMA_26'] = df['close'].ewm(span=26, adjust=False).mean()
        
        # RSI (Relative Strength Index)
        df['RSI'] = self._calculate_rsi(df['close'])
        
        # MACD
        df['MACD'] = df['EMA_12'] - df['EMA_26']
        df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
        
        # Bollinger Bands
        bb_period = 20
        df['BB_Middle'] = df['close'].rolling(window=bb_period).mean()
        bb_std = df['close'].rolling(window=bb_period).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
        
        # Volume indicators
        df['Volume_SMA'] = df['volume'].rolling(window=20).mean()
        df['Volume_Ratio'] = df['volume'] / df['Volume_SMA']
        
        # ATR (Average True Range)
        df['ATR'] = self._calculate_atr(df)
        
        # Momentum
        df['Momentum'] = df['close'] - df['close'].shift(10)
        
        # Rate of Change
        df['ROC'] = ((df['close'] - df['close'].shift(10)) / df['close'].shift(10)) * 100
        
        return df
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_atr(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Average True Range"""
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        atr = true_range.rolling(window=period).mean()
        
        return atr
    
    def generate_signals(self, df: pd.DataFrame) -> Dict[str, any]:
        """
        Generate trading signals based on technical analysis
        
        Args:
            df: DataFrame with calculated indicators
            
        Returns:
            Dictionary with signal information
        """
        if len(df) < 50:
            return {'signal': 'HOLD', 'confidence': 0.0, 'reason': 'Insufficient data'}
        
        signals = []
        reasons = []
        
        # RSI signals
        current_rsi = df['RSI'].iloc[-1]
        if current_rsi < 30:
            signals.append(1)  # Buy
            reasons.append('RSI oversold')
        elif current_rsi > 70:
            signals.append(-1)  # Sell
            reasons.append('RSI overbought')
        else:
            signals.append(0)  # Neutral
        
        # MACD signals
        if df['MACD'].iloc[-1] > df['MACD_Signal'].iloc[-1] and df['MACD'].iloc[-2] <= df['MACD_Signal'].iloc[-2]:
            signals.append(1)  # Buy
            reasons.append('MACD bullish crossover')
        elif df['MACD'].iloc[-1] < df['MACD_Signal'].iloc[-1] and df['MACD'].iloc[-2] >= df['MACD_Signal'].iloc[-2]:
            signals.append(-1)  # Sell
            reasons.append('MACD bearish crossover')
        else:
            signals.append(0)
        
        # Moving Average signals
        if df['SMA_20'].iloc[-1] > df['SMA_50'].iloc[-1] and df['SMA_20'].iloc[-2] <= df['SMA_50'].iloc[-2]:
            signals.append(1)  # Buy
            reasons.append('Golden cross (SMA)')
        elif df['SMA_20'].iloc[-1] < df['SMA_50'].iloc[-1] and df['SMA_20'].iloc[-2] >= df['SMA_50'].iloc[-2]:
            signals.append(-1)  # Sell
            reasons.append('Death cross (SMA)')
        else:
            signals.append(0)
        
        # Bollinger Bands signals
        current_price = df['close'].iloc[-1]
        if current_price <= df['BB_Lower'].iloc[-1]:
            signals.append(1)  # Buy
            reasons.append('Price at lower Bollinger Band')
        elif current_price >= df['BB_Upper'].iloc[-1]:
            signals.append(-1)  # Sell
            reasons.append('Price at upper Bollinger Band')
        else:
            signals.append(0)
        
        # Aggregate signals
        signal_sum = sum(signals)
        signal_count = len([s for s in signals if s != 0])
        
        if signal_sum > 1:
            signal = 'BUY'
            confidence = min(signal_sum / len(signals), 1.0)
        elif signal_sum < -1:
            signal = 'SELL'
            confidence = min(abs(signal_sum) / len(signals), 1.0)
        else:
            signal = 'HOLD'
            confidence = 0.5
        
        return {
            'signal': signal,
            'confidence': confidence,
            'reasons': [r for r in reasons if r],
            'indicators': {
                'RSI': current_rsi,
                'MACD': df['MACD'].iloc[-1],
                'MACD_Signal': df['MACD_Signal'].iloc[-1],
                'SMA_20': df['SMA_20'].iloc[-1],
                'SMA_50': df['SMA_50'].iloc[-1],
                'BB_Upper': df['BB_Upper'].iloc[-1],
                'BB_Lower': df['BB_Lower'].iloc[-1],
                'current_price': current_price
            }
        }
    
    def train_ml_model(self, historical_data: pd.DataFrame, labels: np.ndarray):
        """
        Train ML model for pattern recognition
        
        Args:
            historical_data: Historical price data with indicators
            labels: Trading outcome labels (1: profit, 0: loss)
        """
        features = self._extract_features(historical_data)
        features_scaled = self.scaler.fit_transform(features)
        
        self.ml_model.fit(features_scaled, labels)
    
    def _extract_features(self, df: pd.DataFrame) -> np.ndarray:
        """Extract features for ML model"""
        feature_columns = ['RSI', 'MACD', 'MACD_Hist', 'Volume_Ratio', 'ATR', 'Momentum', 'ROC']
        
        features = df[feature_columns].fillna(0).values
        return features
    
    def predict_with_ml(self, df: pd.DataFrame) -> Dict[str, any]:
        """
        Use ML model to predict trading signal
        
        Args:
            df: DataFrame with calculated indicators
            
        Returns:
            Prediction dictionary
        """
        if self.ml_model is None:
            return {'prediction': 'HOLD', 'confidence': 0.0}
        
        features = self._extract_features(df.tail(1))
        features_scaled = self.scaler.transform(features)
        
        try:
            prediction = self.ml_model.predict(features_scaled)[0]
            probabilities = self.ml_model.predict_proba(features_scaled)[0]
            confidence = max(probabilities)
            
            signal = 'BUY' if prediction == 1 else 'SELL' if prediction == 0 else 'HOLD'
            
            return {
                'prediction': signal,
                'confidence': confidence,
                'probabilities': probabilities.tolist()
            }
        except Exception as e:
            return {'prediction': 'HOLD', 'confidence': 0.0, 'error': str(e)}
