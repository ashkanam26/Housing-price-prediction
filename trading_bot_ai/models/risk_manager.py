"""
AI-based Risk Management Module
"""

import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class RiskManager:
    """AI-based risk management for trading"""
    
    def __init__(self, config: Dict):
        """
        Initialize risk manager
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.risk_config = config.get('risk_management', {})
        
        self.max_daily_loss = self.risk_config.get('max_daily_loss', 0.05)
        self.max_open_positions = self.risk_config.get('max_open_positions', 3)
        self.risk_per_trade = self.risk_config.get('risk_per_trade', 0.02)
        self.use_ai_assessment = self.risk_config.get('use_ai_risk_assessment', True)
        
        # Track daily performance
        self.daily_pnl = 0.0
        self.daily_trades = []
        self.current_date = datetime.now().date()
        
        # Position tracking
        self.open_positions = []
    
    def reset_daily_metrics(self):
        """Reset daily metrics at the start of a new day"""
        current_date = datetime.now().date()
        if current_date != self.current_date:
            self.current_date = current_date
            self.daily_pnl = 0.0
            self.daily_trades = []
    
    def can_open_position(self, capital: float) -> Dict[str, any]:
        """
        Check if a new position can be opened
        
        Args:
            capital: Current capital
            
        Returns:
            Dictionary with decision and reason
        """
        self.reset_daily_metrics()
        
        # Check daily loss limit
        if self.daily_pnl < -(capital * self.max_daily_loss):
            return {
                'allowed': False,
                'reason': f'Daily loss limit reached ({self.max_daily_loss*100:.1f}%)',
                'restriction': 'daily_loss_limit'
            }
        
        # Check max open positions
        if len(self.open_positions) >= self.max_open_positions:
            return {
                'allowed': False,
                'reason': f'Maximum open positions reached ({self.max_open_positions})',
                'restriction': 'max_positions'
            }
        
        return {
            'allowed': True,
            'reason': 'No restrictions',
            'restriction': None
        }
    
    def calculate_position_size(
        self,
        capital: float,
        entry_price: float,
        stop_loss_price: float,
        risk_score: float = 0.5
    ) -> Dict[str, any]:
        """
        Calculate position size based on risk parameters
        
        Args:
            capital: Current capital
            entry_price: Entry price
            stop_loss_price: Stop loss price
            risk_score: Risk score from 0 (low) to 1 (high)
            
        Returns:
            Position sizing information
        """
        # Base risk amount
        risk_amount = capital * self.risk_per_trade
        
        # Adjust for AI risk assessment
        if self.use_ai_assessment:
            # Higher risk score means smaller position
            risk_adjustment = 1.0 - (risk_score * 0.5)  # Reduce by up to 50%
            risk_amount *= risk_adjustment
        
        # Calculate position size based on stop loss
        price_risk = abs(entry_price - stop_loss_price)
        if price_risk > 0:
            position_size = risk_amount / price_risk
        else:
            position_size = 0
        
        # Apply maximum position size limit
        max_position_value = capital * self.config.get('trading', {}).get('max_position_size', 0.1)
        max_size = max_position_value / entry_price
        
        position_size = min(position_size, max_size)
        position_value = position_size * entry_price
        
        return {
            'position_size': position_size,
            'position_value': position_value,
            'risk_amount': risk_amount,
            'risk_percentage': (risk_amount / capital) * 100,
            'stop_loss_price': stop_loss_price,
            'entry_price': entry_price
        }
    
    def calculate_stop_loss(
        self,
        entry_price: float,
        position_type: str,
        atr: float = None,
        support_level: float = None
    ) -> float:
        """
        Calculate stop loss price
        
        Args:
            entry_price: Entry price
            position_type: 'long' or 'short'
            atr: Average True Range (optional)
            support_level: Support level (optional)
            
        Returns:
            Stop loss price
        """
        stop_loss_pct = self.config.get('trading', {}).get('stop_loss_pct', 0.02)
        
        if position_type == 'long':
            # Use ATR-based stop loss if available
            if atr:
                stop_loss = entry_price - (2 * atr)
            # Use support level if available and makes sense
            elif support_level and support_level < entry_price:
                stop_loss = support_level * 0.99  # Slightly below support
            else:
                # Use percentage-based stop loss
                stop_loss = entry_price * (1 - stop_loss_pct)
        else:  # short
            if atr:
                stop_loss = entry_price + (2 * atr)
            else:
                stop_loss = entry_price * (1 + stop_loss_pct)
        
        return stop_loss
    
    def calculate_take_profit(
        self,
        entry_price: float,
        position_type: str,
        resistance_level: float = None
    ) -> List[float]:
        """
        Calculate take profit levels
        
        Args:
            entry_price: Entry price
            position_type: 'long' or 'short'
            resistance_level: Resistance level (optional)
            
        Returns:
            List of take profit prices
        """
        take_profit_pct = self.config.get('trading', {}).get('take_profit_pct', 0.05)
        
        # Multiple take profit levels
        tp_levels = []
        
        if position_type == 'long':
            tp_levels = [
                entry_price * (1 + take_profit_pct * 0.6),  # 60% of target
                entry_price * (1 + take_profit_pct),        # 100% of target
                entry_price * (1 + take_profit_pct * 1.6)   # 160% of target
            ]
            
            # Adjust if resistance level is available
            if resistance_level and resistance_level > entry_price:
                tp_levels[0] = min(tp_levels[0], resistance_level * 0.99)
        else:  # short
            tp_levels = [
                entry_price * (1 - take_profit_pct * 0.6),
                entry_price * (1 - take_profit_pct),
                entry_price * (1 - take_profit_pct * 1.6)
            ]
        
        return tp_levels
    
    def assess_trade_risk(
        self,
        signal_data: Dict,
        market_data: Dict,
        sentiment_data: Dict
    ) -> Dict[str, any]:
        """
        AI-based comprehensive risk assessment for a trade
        
        Args:
            signal_data: Trading signal data
            market_data: Current market data
            sentiment_data: Sentiment analysis data
            
        Returns:
            Risk assessment
        """
        risk_factors = []
        risk_score = 0.0
        
        # Technical signal confidence
        technical_confidence = signal_data.get('confidence', 0.5)
        if technical_confidence < 0.6:
            risk_factors.append('Low technical confidence')
            risk_score += 0.2
        
        # Volatility risk
        volatility = market_data.get('volatility', 0)
        if volatility > 0.5:
            risk_factors.append('High volatility')
            risk_score += 0.15
        
        # Volume risk
        volume_ratio = market_data.get('volume_ratio', 1.0)
        if volume_ratio < 0.5:
            risk_factors.append('Low trading volume')
            risk_score += 0.1
        
        # Sentiment risk
        sentiment_score = sentiment_data.get('sentiment_score', 0.5)
        sentiment_confidence = sentiment_data.get('confidence', 0.5)
        
        # Conflicting sentiment and signal
        signal_direction = signal_data.get('signal', 'HOLD')
        if signal_direction == 'BUY' and sentiment_score < 0.4:
            risk_factors.append('Negative sentiment conflicts with buy signal')
            risk_score += 0.15
        elif signal_direction == 'SELL' and sentiment_score > 0.6:
            risk_factors.append('Positive sentiment conflicts with sell signal')
            risk_score += 0.15
        
        # Low sentiment confidence
        if sentiment_confidence < 0.5:
            risk_factors.append('Low sentiment confidence')
            risk_score += 0.1
        
        # Market conditions
        trend = market_data.get('trend', 'neutral')
        if trend == 'strong_downtrend' and signal_direction == 'BUY':
            risk_factors.append('Buying against strong downtrend')
            risk_score += 0.2
        elif trend == 'strong_uptrend' and signal_direction == 'SELL':
            risk_factors.append('Selling against strong uptrend')
            risk_score += 0.2
        
        # Cap risk score at 1.0
        risk_score = min(risk_score, 1.0)
        
        # Determine risk level
        if risk_score > 0.7:
            risk_level = 'HIGH'
            recommendation = 'AVOID'
        elif risk_score > 0.5:
            risk_level = 'MEDIUM'
            recommendation = 'REDUCE_SIZE'
        elif risk_score > 0.3:
            risk_level = 'LOW-MEDIUM'
            recommendation = 'PROCEED_WITH_CAUTION'
        else:
            risk_level = 'LOW'
            recommendation = 'PROCEED'
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'risk_factors': risk_factors,
            'recommendation': recommendation,
            'position_size_multiplier': max(0.3, 1.0 - risk_score)  # Reduce size for higher risk
        }
    
    def update_position(self, position_id: str, pnl: float):
        """Update position with P&L"""
        self.daily_pnl += pnl
        self.daily_trades.append({
            'position_id': position_id,
            'pnl': pnl,
            'timestamp': datetime.now()
        })
    
    def add_position(self, position: Dict):
        """Add new open position"""
        self.open_positions.append(position)
    
    def remove_position(self, position_id: str):
        """Remove closed position"""
        self.open_positions = [p for p in self.open_positions if p.get('id') != position_id]
    
    def get_daily_summary(self) -> Dict[str, any]:
        """Get daily performance summary"""
        self.reset_daily_metrics()
        
        return {
            'date': self.current_date.isoformat(),
            'total_pnl': self.daily_pnl,
            'total_trades': len(self.daily_trades),
            'open_positions': len(self.open_positions),
            'winning_trades': len([t for t in self.daily_trades if t['pnl'] > 0]),
            'losing_trades': len([t for t in self.daily_trades if t['pnl'] < 0])
        }
