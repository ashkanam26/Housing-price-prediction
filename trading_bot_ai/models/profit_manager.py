"""
AI-based Profit Management Module
"""

import numpy as np
from typing import Dict, List, Optional
from datetime import datetime


class ProfitManager:
    """AI-based profit management for trading"""
    
    def __init__(self, config: Dict):
        """
        Initialize profit manager
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.profit_config = config.get('profit_management', {})
        
        self.trailing_stop = self.profit_config.get('trailing_stop', True)
        self.trailing_stop_pct = self.profit_config.get('trailing_stop_pct', 0.03)
        self.partial_profit_taking = self.profit_config.get('partial_profit_taking', True)
        self.profit_levels = self.profit_config.get('profit_levels', [0.03, 0.05, 0.08])
        
        # Track positions and their profit states
        self.position_states = {}
    
    def should_take_profit(
        self,
        position: Dict,
        current_price: float,
        market_data: Dict
    ) -> Dict[str, any]:
        """
        Determine if profit should be taken
        
        Args:
            position: Position information
            current_price: Current market price
            market_data: Current market data
            
        Returns:
            Profit taking decision
        """
        entry_price = position.get('entry_price')
        position_type = position.get('type', 'long')
        position_id = position.get('id')
        
        # Calculate current profit percentage
        if position_type == 'long':
            profit_pct = (current_price - entry_price) / entry_price
        else:  # short
            profit_pct = (entry_price - current_price) / entry_price
        
        # Initialize position state if not exists
        if position_id not in self.position_states:
            self.position_states[position_id] = {
                'highest_price': current_price if position_type == 'long' else None,
                'lowest_price': current_price if position_type == 'short' else None,
                'profit_levels_taken': [],
                'trailing_stop_active': False,
                'trailing_stop_price': None
            }
        
        state = self.position_states[position_id]
        decision = {
            'take_profit': False,
            'percentage': 0.0,
            'reason': '',
            'new_stop_loss': None
        }
        
        # Update highest/lowest price
        if position_type == 'long':
            if state['highest_price'] is None or current_price > state['highest_price']:
                state['highest_price'] = current_price
        else:
            if state['lowest_price'] is None or current_price < state['lowest_price']:
                state['lowest_price'] = current_price
        
        # Check partial profit taking levels
        if self.partial_profit_taking:
            for level in self.profit_levels:
                if profit_pct >= level and level not in state['profit_levels_taken']:
                    # Take partial profit at this level
                    percentage = self._calculate_partial_profit_percentage(level)
                    decision['take_profit'] = True
                    decision['percentage'] = percentage
                    decision['reason'] = f'Partial profit at {level*100:.1f}% level'
                    state['profit_levels_taken'].append(level)
                    
                    # Activate trailing stop after first profit level
                    if not state['trailing_stop_active']:
                        state['trailing_stop_active'] = True
                    
                    return decision
        
        # Check trailing stop
        if self.trailing_stop and state['trailing_stop_active']:
            if position_type == 'long':
                # Calculate trailing stop price
                trailing_price = state['highest_price'] * (1 - self.trailing_stop_pct)
                state['trailing_stop_price'] = trailing_price
                
                if current_price <= trailing_price:
                    decision['take_profit'] = True
                    decision['percentage'] = 1.0  # Close entire position
                    decision['reason'] = f'Trailing stop triggered at {self.trailing_stop_pct*100:.1f}%'
                    return decision
            else:  # short
                trailing_price = state['lowest_price'] * (1 + self.trailing_stop_pct)
                state['trailing_stop_price'] = trailing_price
                
                if current_price >= trailing_price:
                    decision['take_profit'] = True
                    decision['percentage'] = 1.0
                    decision['reason'] = f'Trailing stop triggered at {self.trailing_stop_pct*100:.1f}%'
                    return decision
        
        # Check reversal signals from market data
        reversal_detected = self._detect_reversal(market_data, position_type)
        if reversal_detected and profit_pct > 0.02:  # At least 2% profit
            decision['take_profit'] = True
            decision['percentage'] = 1.0
            decision['reason'] = 'Potential reversal detected with profit'
            return decision
        
        # Dynamic profit taking based on market conditions
        volatility = market_data.get('volatility', 0)
        if profit_pct > 0.05 and volatility > 0.6:  # High volatility with good profit
            decision['take_profit'] = True
            decision['percentage'] = 0.5  # Take half
            decision['reason'] = 'Securing profit in high volatility'
            return decision
        
        return decision
    
    def _calculate_partial_profit_percentage(self, profit_level: float) -> float:
        """Calculate what percentage of position to close at profit level"""
        # Progressive profit taking: more aggressive at higher levels
        if profit_level <= 0.03:
            return 0.33  # 33% at first level
        elif profit_level <= 0.05:
            return 0.50  # 50% of remaining at second level
        else:
            return 0.75  # 75% of remaining at third level
    
    def _detect_reversal(self, market_data: Dict, position_type: str) -> bool:
        """Detect potential price reversal"""
        # Check RSI
        rsi = market_data.get('RSI')
        if rsi:
            if position_type == 'long' and rsi > 75:
                return True
            elif position_type == 'short' and rsi < 25:
                return True
        
        # Check MACD divergence or crossover
        macd_signal = market_data.get('MACD_signal')
        if macd_signal:
            if position_type == 'long' and macd_signal == 'bearish_crossover':
                return True
            elif position_type == 'short' and macd_signal == 'bullish_crossover':
                return True
        
        # Check volume decline
        volume_ratio = market_data.get('volume_ratio', 1.0)
        if volume_ratio < 0.5:  # Significant volume decline
            return True
        
        return False
    
    def update_trailing_stop(
        self,
        position_id: str,
        current_price: float,
        position_type: str
    ) -> Optional[float]:
        """
        Update trailing stop for a position
        
        Args:
            position_id: Position identifier
            current_price: Current market price
            position_type: 'long' or 'short'
            
        Returns:
            New trailing stop price or None
        """
        if position_id not in self.position_states:
            return None
        
        state = self.position_states[position_id]
        
        if not state['trailing_stop_active']:
            return None
        
        if position_type == 'long':
            if state['highest_price'] is None or current_price > state['highest_price']:
                state['highest_price'] = current_price
                state['trailing_stop_price'] = current_price * (1 - self.trailing_stop_pct)
                return state['trailing_stop_price']
        else:  # short
            if state['lowest_price'] is None or current_price < state['lowest_price']:
                state['lowest_price'] = current_price
                state['trailing_stop_price'] = current_price * (1 + self.trailing_stop_pct)
                return state['trailing_stop_price']
        
        return state.get('trailing_stop_price')
    
    def calculate_optimal_exit(
        self,
        position: Dict,
        current_price: float,
        market_data: Dict,
        sentiment_data: Dict
    ) -> Dict[str, any]:
        """
        AI-based calculation of optimal exit strategy
        
        Args:
            position: Position information
            current_price: Current price
            market_data: Market analysis data
            sentiment_data: Sentiment analysis data
            
        Returns:
            Optimal exit strategy
        """
        entry_price = position.get('entry_price')
        position_type = position.get('type', 'long')
        
        # Calculate current profit
        if position_type == 'long':
            profit_pct = (current_price - entry_price) / entry_price
        else:
            profit_pct = (entry_price - current_price) / entry_price
        
        scores = []
        reasons = []
        
        # Profit level score
        if profit_pct > 0.08:
            scores.append(0.9)
            reasons.append('Strong profit reached')
        elif profit_pct > 0.05:
            scores.append(0.7)
            reasons.append('Good profit reached')
        elif profit_pct > 0.02:
            scores.append(0.5)
            reasons.append('Moderate profit')
        else:
            scores.append(0.3)
        
        # Technical indicators score
        rsi = market_data.get('RSI', 50)
        if position_type == 'long':
            if rsi > 70:
                scores.append(0.8)
                reasons.append('Overbought RSI')
            elif rsi > 60:
                scores.append(0.6)
        else:  # short
            if rsi < 30:
                scores.append(0.8)
                reasons.append('Oversold RSI')
            elif rsi < 40:
                scores.append(0.6)
        
        # Sentiment shift score
        sentiment_score = sentiment_data.get('sentiment_score', 0.5)
        if position_type == 'long' and sentiment_score < 0.4:
            scores.append(0.7)
            reasons.append('Sentiment turning negative')
        elif position_type == 'short' and sentiment_score > 0.6:
            scores.append(0.7)
            reasons.append('Sentiment turning positive')
        else:
            scores.append(0.3)
        
        # Market condition score
        trend = market_data.get('trend', 'neutral')
        if (position_type == 'long' and trend == 'downtrend') or \
           (position_type == 'short' and trend == 'uptrend'):
            scores.append(0.8)
            reasons.append('Trend reversal detected')
        else:
            scores.append(0.3)
        
        # Calculate exit score
        exit_score = np.mean(scores)
        
        # Determine recommendation
        if exit_score > 0.7:
            recommendation = 'EXIT_NOW'
            urgency = 'high'
        elif exit_score > 0.5:
            recommendation = 'CONSIDER_EXIT'
            urgency = 'medium'
        else:
            recommendation = 'HOLD'
            urgency = 'low'
        
        return {
            'recommendation': recommendation,
            'exit_score': exit_score,
            'urgency': urgency,
            'reasons': reasons,
            'current_profit_pct': profit_pct * 100,
            'suggested_action': self._get_exit_action(exit_score, profit_pct)
        }
    
    def _get_exit_action(self, exit_score: float, profit_pct: float) -> str:
        """Get specific exit action recommendation"""
        if exit_score > 0.7:
            if profit_pct > 0:
                return 'Close position and secure profit'
            else:
                return 'Close position to limit loss'
        elif exit_score > 0.5:
            if profit_pct > 0.03:
                return 'Consider taking partial profit (50%)'
            else:
                return 'Move stop loss to break even'
        else:
            if profit_pct > 0.05:
                return 'Activate trailing stop to protect profit'
            else:
                return 'Continue holding with current stop loss'
    
    def get_position_state(self, position_id: str) -> Optional[Dict]:
        """Get current state of a position"""
        return self.position_states.get(position_id)
    
    def remove_position_state(self, position_id: str):
        """Remove position state when position is closed"""
        if position_id in self.position_states:
            del self.position_states[position_id]
    
    def get_profit_summary(self) -> Dict[str, any]:
        """Get summary of profit management status"""
        active_positions = len(self.position_states)
        trailing_stops_active = sum(
            1 for state in self.position_states.values() 
            if state.get('trailing_stop_active', False)
        )
        
        return {
            'active_positions': active_positions,
            'trailing_stops_active': trailing_stops_active,
            'partial_profits_taken': sum(
                len(state.get('profit_levels_taken', [])) 
                for state in self.position_states.values()
            )
        }
