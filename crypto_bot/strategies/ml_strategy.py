"""
Trading Strategy Engine
Combines ML predictions, sentiment analysis, and technical indicators
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')


class TradingStrategy:
    """
    Advanced trading strategy combining multiple signals
    """
    
    def __init__(self, initial_capital: float = 10000, 
                 risk_per_trade: float = 0.02,
                 stop_loss_pct: float = 0.03,
                 take_profit_pct: float = 0.06):
        """
        Initialize trading strategy
        
        Args:
            initial_capital: Starting capital in USDT
            risk_per_trade: Maximum risk per trade (2% default)
            stop_loss_pct: Stop loss percentage (3% default)
            take_profit_pct: Take profit percentage (6% default)
        """
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.risk_per_trade = risk_per_trade
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct
        
        self.position = None  # Current position {'side': 'long/short', 'amount': x, 'entry_price': y}
        self.trades_history = []
        self.equity_curve = []
        
    def calculate_position_size(self, entry_price: float, 
                               stop_loss_price: float) -> float:
        """
        Calculate position size based on risk management
        
        Args:
            entry_price: Entry price for the trade
            stop_loss_price: Stop loss price
            
        Returns:
            Position size (amount to trade)
        """
        risk_amount = self.current_capital * self.risk_per_trade
        price_risk = abs(entry_price - stop_loss_price)
        
        if price_risk == 0:
            return 0
        
        position_size = risk_amount / price_risk
        
        # Ensure we don't use more than available capital
        max_position = (self.current_capital * 0.95) / entry_price
        position_size = min(position_size, max_position)
        
        return position_size
    
    def combine_signals(self, price_signal: str, sentiment_signal: str,
                       df: pd.DataFrame) -> Dict:
        """
        Combine multiple trading signals
        
        Args:
            price_signal: Signal from price prediction model
            sentiment_signal: Signal from sentiment analysis
            df: DataFrame with technical indicators
            
        Returns:
            Dictionary with combined signal and confidence
        """
        signals = []
        weights = []
        
        # Price prediction signal (weight: 40%)
        if price_signal == 'BUY':
            signals.append(1)
            weights.append(0.4)
        elif price_signal == 'SELL':
            signals.append(-1)
            weights.append(0.4)
        else:
            signals.append(0)
            weights.append(0.4)
        
        # Sentiment signal (weight: 30%)
        if sentiment_signal == 'BUY':
            signals.append(1)
            weights.append(0.3)
        elif sentiment_signal == 'SELL':
            signals.append(-1)
            weights.append(0.3)
        else:
            signals.append(0)
            weights.append(0.3)
        
        # Technical indicators signal (weight: 30%)
        tech_signal = self._technical_signal(df)
        signals.append(tech_signal)
        weights.append(0.3)
        
        # Calculate weighted average
        combined_score = sum(s * w for s, w in zip(signals, weights))
        
        # Determine action
        if combined_score > 0.3:
            action = 'BUY'
            confidence = min(combined_score, 1.0)
        elif combined_score < -0.3:
            action = 'SELL'
            confidence = min(abs(combined_score), 1.0)
        else:
            action = 'HOLD'
            confidence = 0.5
        
        return {
            'action': action,
            'confidence': confidence,
            'score': combined_score,
            'price_signal': price_signal,
            'sentiment_signal': sentiment_signal,
            'technical_signal': 'BUY' if tech_signal > 0 else 'SELL' if tech_signal < 0 else 'HOLD'
        }
    
    def _technical_signal(self, df: pd.DataFrame) -> float:
        """
        Generate signal from technical indicators
        
        Args:
            df: DataFrame with technical indicators
            
        Returns:
            Signal score (-1 to 1)
        """
        if len(df) == 0:
            return 0
        
        last_row = df.iloc[-1]
        score = 0
        
        # RSI signal
        if 'rsi' in df.columns:
            rsi = last_row['rsi']
            if rsi < 30:
                score += 0.3  # Oversold - buy signal
            elif rsi > 70:
                score -= 0.3  # Overbought - sell signal
        
        # MACD signal
        if 'macd' in df.columns and 'macd_signal' in df.columns:
            if last_row['macd'] > last_row['macd_signal']:
                score += 0.3
            else:
                score -= 0.3
        
        # Moving average signal
        if 'sma_7' in df.columns and 'sma_25' in df.columns:
            if last_row['sma_7'] > last_row['sma_25']:
                score += 0.2
            else:
                score -= 0.2
        
        # Bollinger Bands signal
        if 'bb_upper' in df.columns and 'bb_lower' in df.columns:
            price = last_row['close']
            if price <= last_row['bb_lower']:
                score += 0.2  # At lower band - buy signal
            elif price >= last_row['bb_upper']:
                score -= 0.2  # At upper band - sell signal
        
        return np.clip(score, -1, 1)
    
    def execute_trade(self, signal: Dict, current_price: float, 
                     timestamp: datetime) -> Optional[Dict]:
        """
        Execute trade based on signal
        
        Args:
            signal: Combined trading signal
            current_price: Current market price
            timestamp: Current timestamp
            
        Returns:
            Trade execution details or None
        """
        action = signal['action']
        
        # Close existing position if signal reverses
        if self.position is not None:
            if (self.position['side'] == 'long' and action == 'SELL') or \
               (self.position['side'] == 'short' and action == 'BUY'):
                return self._close_position(current_price, timestamp, 'signal_reverse')
        
        # Open new position
        if self.position is None and action in ['BUY', 'SELL']:
            if signal['confidence'] > 0.6:  # Only trade with high confidence
                return self._open_position(action, current_price, timestamp)
        
        return None
    
    def _open_position(self, side: str, entry_price: float, 
                      timestamp: datetime) -> Dict:
        """Open a new position"""
        # Calculate stop loss and take profit
        if side == 'BUY':
            stop_loss = entry_price * (1 - self.stop_loss_pct)
            take_profit = entry_price * (1 + self.take_profit_pct)
        else:  # SELL (short)
            stop_loss = entry_price * (1 + self.stop_loss_pct)
            take_profit = entry_price * (1 - self.take_profit_pct)
        
        # Calculate position size
        position_size = self.calculate_position_size(entry_price, stop_loss)
        
        if position_size <= 0:
            return None
        
        self.position = {
            'side': 'long' if side == 'BUY' else 'short',
            'amount': position_size,
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'entry_time': timestamp
        }
        
        trade = {
            'timestamp': timestamp,
            'action': 'OPEN',
            'side': self.position['side'],
            'amount': position_size,
            'price': entry_price,
            'capital': self.current_capital
        }
        
        self.trades_history.append(trade)
        
        return trade
    
    def _close_position(self, exit_price: float, timestamp: datetime, 
                       reason: str) -> Dict:
        """Close existing position"""
        if self.position is None:
            return None
        
        entry_price = self.position['entry_price']
        amount = self.position['amount']
        side = self.position['side']
        
        # Calculate profit/loss
        if side == 'long':
            pnl = (exit_price - entry_price) * amount
        else:  # short
            pnl = (entry_price - exit_price) * amount
        
        pnl_pct = (pnl / (entry_price * amount)) * 100
        
        # Update capital
        self.current_capital += pnl
        
        trade = {
            'timestamp': timestamp,
            'action': 'CLOSE',
            'side': side,
            'amount': amount,
            'entry_price': entry_price,
            'exit_price': exit_price,
            'pnl': pnl,
            'pnl_pct': pnl_pct,
            'capital': self.current_capital,
            'reason': reason
        }
        
        self.trades_history.append(trade)
        self.equity_curve.append({
            'timestamp': timestamp,
            'equity': self.current_capital
        })
        
        self.position = None
        
        return trade
    
    def check_stop_loss_take_profit(self, current_price: float, 
                                    timestamp: datetime) -> Optional[Dict]:
        """Check if stop loss or take profit is hit"""
        if self.position is None:
            return None
        
        side = self.position['side']
        stop_loss = self.position['stop_loss']
        take_profit = self.position['take_profit']
        
        if side == 'long':
            if current_price <= stop_loss:
                return self._close_position(current_price, timestamp, 'stop_loss')
            elif current_price >= take_profit:
                return self._close_position(current_price, timestamp, 'take_profit')
        else:  # short
            if current_price >= stop_loss:
                return self._close_position(current_price, timestamp, 'stop_loss')
            elif current_price <= take_profit:
                return self._close_position(current_price, timestamp, 'take_profit')
        
        return None
    
    def get_performance_metrics(self) -> Dict:
        """Calculate strategy performance metrics"""
        if len(self.trades_history) == 0:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0,
                'total_return': 0,
                'total_return_pct': 0
            }
        
        closed_trades = [t for t in self.trades_history if t['action'] == 'CLOSE']
        
        winning_trades = [t for t in closed_trades if t['pnl'] > 0]
        losing_trades = [t for t in closed_trades if t['pnl'] < 0]
        
        total_return = self.current_capital - self.initial_capital
        total_return_pct = (total_return / self.initial_capital) * 100
        
        avg_win = np.mean([t['pnl'] for t in winning_trades]) if winning_trades else 0
        avg_loss = np.mean([t['pnl'] for t in losing_trades]) if losing_trades else 0
        
        return {
            'total_trades': len(closed_trades),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': (len(winning_trades) / len(closed_trades) * 100) if closed_trades else 0,
            'total_return': total_return,
            'total_return_pct': total_return_pct,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'current_capital': self.current_capital,
            'max_equity': max([e['equity'] for e in self.equity_curve]) if self.equity_curve else self.initial_capital
        }


if __name__ == "__main__":
    # Example usage
    strategy = TradingStrategy(initial_capital=10000)
    
    # Simulate some signals
    signal = {
        'action': 'BUY',
        'confidence': 0.75,
        'score': 0.65,
        'price_signal': 'BUY',
        'sentiment_signal': 'BUY',
        'technical_signal': 'BUY'
    }
    
    current_price = 50000
    timestamp = datetime.now()
    
    # Execute trade
    trade = strategy.execute_trade(signal, current_price, timestamp)
    print(f"Trade executed: {trade}")
    
    # Check performance
    metrics = strategy.get_performance_metrics()
    print(f"\nPerformance Metrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
