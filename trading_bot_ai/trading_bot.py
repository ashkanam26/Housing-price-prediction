"""
Main Trading Bot Orchestrator
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime

from .config import Config
from .analyzers import (
    TechnicalAnalyzer,
    FundamentalAnalyzer,
    SentimentAnalyzer,
    NewsAnalyzer
)
from .models import RiskManager, ProfitManager
from .data_collectors import (
    MarketDataCollector,
    NewsCollector,
    SentimentCollector
)


class TradingBot:
    """AI-powered cryptocurrency trading bot"""
    
    def __init__(self, config_path: str = None):
        """
        Initialize trading bot
        
        Args:
            config_path: Path to configuration file
        """
        # Setup logging
        self.logger = logging.getLogger('TradingBot')
        self.logger.setLevel(logging.INFO)
        
        # Load configuration
        self.config = Config(config_path)
        
        # Initialize components
        self._initialize_components()
        
        # Trading state
        self.is_running = False
        self.capital = self.config.get('trading.initial_capital', 10000)
        self.positions = []
        
        self.logger.info("Trading Bot initialized successfully")
    
    def _initialize_components(self):
        """Initialize all bot components"""
        config_dict = self.config.settings
        
        # Data collectors
        self.market_data = MarketDataCollector(config_dict)
        self.news_collector = NewsCollector(config_dict)
        self.sentiment_collector = SentimentCollector(config_dict)
        
        # Analyzers
        self.technical_analyzer = TechnicalAnalyzer(config_dict)
        self.fundamental_analyzer = FundamentalAnalyzer(config_dict)
        self.sentiment_analyzer = SentimentAnalyzer(config_dict)
        self.news_analyzer = NewsAnalyzer(config_dict)
        
        # Managers
        self.risk_manager = RiskManager(config_dict)
        self.profit_manager = ProfitManager(config_dict)
    
    def analyze_symbol(self, symbol: str) -> Dict[str, any]:
        """
        Perform comprehensive analysis of a trading symbol
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTC/USDT')
            
        Returns:
            Complete analysis results
        """
        self.logger.info(f"Analyzing {symbol}...")
        
        # 1. Fetch market data
        ohlcv_data = self.market_data.fetch_ohlcv(
            symbol,
            timeframe=self.config.get('trading.timeframe', '1h'),
            limit=self.config.get('technical_analysis.lookback_period', 100)
        )
        
        ticker = self.market_data.fetch_ticker(symbol)
        fundamental_data = self.market_data.fetch_fundamental_data(symbol)
        
        # 2. Technical Analysis
        ohlcv_with_indicators = self.technical_analyzer.calculate_indicators(ohlcv_data)
        technical_signals = self.technical_analyzer.generate_signals(ohlcv_with_indicators)
        
        # 3. Fundamental Analysis
        fundamental_analysis = self.fundamental_analyzer.analyze_fundamentals(fundamental_data)
        risk_assessment = self.fundamental_analyzer.get_risk_assessment(fundamental_data)
        
        # 4. Sentiment Analysis
        social_posts = self.sentiment_collector.fetch_social_media_posts(symbol, limit=100)
        sentiment_analysis = self.sentiment_analyzer.analyze_social_media(social_posts)
        fear_greed = self.sentiment_analyzer.calculate_fear_greed_index(sentiment_analysis)
        
        # 5. News Analysis
        news_items = self.news_collector.fetch_latest_news(symbols=[symbol], limit=50)
        news_analysis = self.news_analyzer.analyze_news_batch(news_items)
        market_events = self.news_analyzer.detect_market_events(news_items)
        
        # 6. Compile results
        analysis = {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'current_price': ticker.get('last_price'),
            'technical': {
                'signal': technical_signals['signal'],
                'confidence': technical_signals['confidence'],
                'reasons': technical_signals['reasons'],
                'indicators': technical_signals['indicators']
            },
            'fundamental': {
                'signal': fundamental_analysis['signal'],
                'score': fundamental_analysis['score'],
                'factors': fundamental_analysis['factors'],
                'risk': risk_assessment
            },
            'sentiment': {
                'signal': sentiment_analysis['signal'],
                'score': sentiment_analysis['score'],
                'distribution': sentiment_analysis['distribution'],
                'fear_greed_index': fear_greed
            },
            'news': {
                'signal': news_analysis['signal'],
                'sentiment': news_analysis['overall_sentiment'],
                'impact': news_analysis['impact_level'],
                'events': market_events[:5]  # Top 5 events
            }
        }
        
        return analysis
    
    def generate_trading_decision(self, analysis: Dict) -> Dict[str, any]:
        """
        Generate final trading decision based on all analyses
        
        Args:
            analysis: Complete analysis results
            
        Returns:
            Trading decision
        """
        symbol = analysis['symbol']
        
        # Collect signals from all analyzers
        signals = {
            'technical': analysis['technical']['signal'],
            'fundamental': analysis['fundamental']['signal'],
            'sentiment': analysis['sentiment']['signal'],
            'news': analysis['news']['signal']
        }
        
        # Collect confidences/scores
        confidences = {
            'technical': analysis['technical']['confidence'],
            'fundamental': analysis['fundamental']['score'],
            'sentiment': analysis['sentiment']['score'],
            'news': analysis['news'].get('confidence', 0.5)
        }
        
        # Weight different signals (can be adjusted)
        weights = {
            'technical': 0.35,
            'fundamental': 0.25,
            'sentiment': 0.20,
            'news': 0.20
        }
        
        # Convert signals to numeric scores
        signal_scores = {
            'technical': self._signal_to_score(signals['technical']),
            'fundamental': self._signal_to_score(signals['fundamental']),
            'sentiment': confidences['sentiment'],
            'news': confidences['news']
        }
        
        # Calculate weighted score
        weighted_score = sum(
            signal_scores[key] * weights[key] * confidences[key]
            for key in signal_scores.keys()
        ) / sum(weights.values())
        
        # Determine final signal
        if weighted_score > 0.65:
            final_signal = 'BUY'
        elif weighted_score < 0.35:
            final_signal = 'SELL'
        else:
            final_signal = 'HOLD'
        
        # Calculate overall confidence
        overall_confidence = sum(confidences.values()) / len(confidences)
        
        # Risk assessment
        market_data = {
            'volatility': analysis['fundamental']['risk']['risk_score'],
            'volume_ratio': 1.0,  # Can be extracted from technical data
            'trend': 'neutral'
        }
        
        sentiment_data = {
            'sentiment_score': analysis['sentiment']['score'],
            'confidence': confidences['sentiment']
        }
        
        signal_data = {
            'signal': final_signal,
            'confidence': overall_confidence
        }
        
        risk_assessment = self.risk_manager.assess_trade_risk(
            signal_data,
            market_data,
            sentiment_data
        )
        
        return {
            'symbol': symbol,
            'decision': final_signal,
            'confidence': overall_confidence,
            'weighted_score': weighted_score,
            'individual_signals': signals,
            'risk_assessment': risk_assessment,
            'timestamp': datetime.now().isoformat()
        }
    
    def _signal_to_score(self, signal: str) -> float:
        """Convert signal string to numeric score"""
        signal_map = {
            'BUY': 1.0,
            'BULLISH': 0.8,
            'HOLD': 0.5,
            'NEUTRAL': 0.5,
            'SELL': 0.0,
            'BEARISH': 0.2
        }
        return signal_map.get(signal.upper(), 0.5)
    
    def execute_trade(self, decision: Dict) -> Dict[str, any]:
        """
        Execute trade based on decision (simulation)
        
        Args:
            decision: Trading decision
            
        Returns:
            Trade execution result
        """
        symbol = decision['symbol']
        signal = decision['decision']
        
        if signal == 'HOLD':
            return {
                'status': 'no_action',
                'message': 'Holding position, no trade executed'
            }
        
        # Check if we can open a position
        can_trade = self.risk_manager.can_open_position(self.capital)
        if not can_trade['allowed']:
            return {
                'status': 'rejected',
                'reason': can_trade['reason']
            }
        
        # Get current price
        ticker = self.market_data.fetch_ticker(symbol)
        current_price = ticker.get('last_price')
        
        # Calculate position size
        risk_score = decision['risk_assessment']['risk_score']
        stop_loss_price = self.risk_manager.calculate_stop_loss(
            current_price,
            'long' if signal == 'BUY' else 'short'
        )
        
        position_info = self.risk_manager.calculate_position_size(
            self.capital,
            current_price,
            stop_loss_price,
            risk_score
        )
        
        # Apply risk-based position size adjustment
        multiplier = decision['risk_assessment'].get('position_size_multiplier', 1.0)
        position_info['position_size'] *= multiplier
        position_info['position_value'] *= multiplier
        
        # Calculate take profit levels
        take_profit_levels = self.risk_manager.calculate_take_profit(
            current_price,
            'long' if signal == 'BUY' else 'short'
        )
        
        # Create position
        position = {
            'id': f"{symbol}_{datetime.now().timestamp()}",
            'symbol': symbol,
            'type': 'long' if signal == 'BUY' else 'short',
            'entry_price': current_price,
            'position_size': position_info['position_size'],
            'position_value': position_info['position_value'],
            'stop_loss': stop_loss_price,
            'take_profit_levels': take_profit_levels,
            'entry_time': datetime.now().isoformat(),
            'status': 'open'
        }
        
        # Add to positions and risk manager
        self.positions.append(position)
        self.risk_manager.add_position(position)
        
        self.logger.info(f"Trade executed: {signal} {symbol} at {current_price}")
        
        return {
            'status': 'executed',
            'position': position,
            'message': f"{signal} order executed successfully"
        }
    
    def run_analysis_cycle(self, symbols: List[str] = None) -> Dict[str, any]:
        """
        Run a complete analysis cycle for configured symbols
        
        Args:
            symbols: List of symbols to analyze (uses config if None)
            
        Returns:
            Analysis results for all symbols
        """
        if symbols is None:
            symbols = self.config.get('trading.symbols', ['BTC/USDT', 'ETH/USDT'])
        
        results = {}
        
        for symbol in symbols:
            try:
                # Analyze symbol
                analysis = self.analyze_symbol(symbol)
                
                # Generate trading decision
                decision = self.generate_trading_decision(analysis)
                
                # Store results
                results[symbol] = {
                    'analysis': analysis,
                    'decision': decision
                }
                
                self.logger.info(
                    f"{symbol}: {decision['decision']} "
                    f"(confidence: {decision['confidence']:.2f})"
                )
                
            except Exception as e:
                self.logger.error(f"Error analyzing {symbol}: {str(e)}")
                results[symbol] = {
                    'error': str(e)
                }
        
        return results
    
    def get_status(self) -> Dict[str, any]:
        """Get current bot status"""
        return {
            'is_running': self.is_running,
            'capital': self.capital,
            'open_positions': len(self.positions),
            'positions': self.positions,
            'daily_summary': self.risk_manager.get_daily_summary(),
            'profit_summary': self.profit_manager.get_profit_summary()
        }
    
    def get_performance_report(self) -> Dict[str, any]:
        """Generate performance report"""
        daily_summary = self.risk_manager.get_daily_summary()
        
        total_trades = daily_summary['total_trades']
        winning_trades = daily_summary['winning_trades']
        losing_trades = daily_summary['losing_trades']
        
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        return {
            'total_capital': self.capital,
            'total_pnl': daily_summary['total_pnl'],
            'pnl_percentage': (daily_summary['total_pnl'] / self.capital * 100),
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'open_positions': len(self.positions),
            'timestamp': datetime.now().isoformat()
        }
