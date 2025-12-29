"""
Main Cryptocurrency Trading Bot
Orchestrates data fetching, prediction, sentiment analysis, and trading
"""

import time
from datetime import datetime
from typing import Dict, Optional
import warnings
warnings.filterwarnings('ignore')

from crypto_bot.data.fetcher import CryptoDataFetcher
from crypto_bot.models.price_predictor import PricePredictionModel
from crypto_bot.models.sentiment_analyzer import SentimentAnalyzer
from crypto_bot.strategies.ml_strategy import TradingStrategy


class CryptoTradingBot:
    """
    Main cryptocurrency trading bot
    Combines ML predictions, NLP sentiment, and trading strategy
    """
    
    def __init__(self, 
                 symbol: str = 'BTC/USDT',
                 initial_capital: float = 10000,
                 timeframe: str = '1h',
                 lookback: int = 60):
        """
        Initialize the trading bot
        
        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            initial_capital: Starting capital
            timeframe: Candle timeframe
            lookback: Number of periods for prediction
        """
        self.symbol = symbol
        self.timeframe = timeframe
        self.initial_capital = initial_capital
        
        # Initialize components
        self.data_fetcher = CryptoDataFetcher()
        self.price_model = PricePredictionModel(lookback=lookback)
        self.sentiment_analyzer = SentimentAnalyzer()
        self.strategy = TradingStrategy(initial_capital=initial_capital)
        
        self.is_running = False
        self.model_trained = False
        
    def train_models(self, historical_periods: int = 500):
        """
        Train ML models with historical data
        
        Args:
            historical_periods: Number of historical periods to fetch
        """
        print(f"Fetching {historical_periods} periods of historical data...")
        df = self.data_fetcher.fetch_ohlcv(
            self.symbol, 
            self.timeframe, 
            historical_periods
        )
        
        print("Adding technical indicators...")
        df = self.data_fetcher.add_technical_indicators(df)
        
        print("Training price prediction model...")
        self.price_model.train(df, epochs=50)
        
        self.model_trained = True
        print("Models trained successfully!")
        
    def get_latest_data(self, periods: int = 100) -> 'pd.DataFrame':
        """
        Get latest market data with indicators
        
        Args:
            periods: Number of periods to fetch
            
        Returns:
            DataFrame with price data and indicators
        """
        df = self.data_fetcher.fetch_ohlcv(self.symbol, self.timeframe, periods)
        df = self.data_fetcher.add_technical_indicators(df)
        return df
    
    def analyze_market(self) -> Dict:
        """
        Perform complete market analysis
        
        Returns:
            Dictionary with analysis results
        """
        # Get latest data
        df = self.get_latest_data(100)
        current_price = df['close'].iloc[-1]
        
        # Get price prediction signal
        price_signal = 'HOLD'
        if self.model_trained:
            price_signal = self.price_model.get_signal(df)
        
        # Get sentiment analysis signal
        sample_texts = self.sentiment_analyzer.generate_sample_texts('mixed', 15)
        sentiment_signal = self.sentiment_analyzer.get_trading_signal(sample_texts)
        market_sentiment = self.sentiment_analyzer.get_market_sentiment(sample_texts)
        
        # Combine signals
        combined_signal = self.strategy.combine_signals(
            price_signal, 
            sentiment_signal, 
            df
        )
        
        # Get technical indicators
        last_row = df.iloc[-1]
        technical_data = {
            'rsi': last_row.get('rsi', None),
            'macd': last_row.get('macd', None),
            'sma_7': last_row.get('sma_7', None),
            'sma_25': last_row.get('sma_25', None),
        }
        
        return {
            'timestamp': datetime.now().isoformat(),
            'symbol': self.symbol,
            'current_price': current_price,
            'price_signal': price_signal,
            'sentiment_signal': sentiment_signal,
            'combined_signal': combined_signal,
            'market_sentiment': market_sentiment,
            'technical_indicators': technical_data,
            'dataframe': df
        }
    
    def run_iteration(self) -> Dict:
        """
        Run one iteration of the trading bot
        
        Returns:
            Dictionary with iteration results
        """
        if not self.model_trained:
            raise ValueError("Models not trained. Call train_models() first.")
        
        # Analyze market
        analysis = self.analyze_market()
        
        current_price = analysis['current_price']
        combined_signal = analysis['combined_signal']
        
        # Check stop loss / take profit
        sl_tp_result = self.strategy.check_stop_loss_take_profit(
            current_price, 
            datetime.now()
        )
        
        # Execute trade based on signal
        trade_result = None
        if sl_tp_result is None:
            trade_result = self.strategy.execute_trade(
                combined_signal,
                current_price,
                datetime.now()
            )
        else:
            trade_result = sl_tp_result
        
        # Get current position and performance
        position = self.strategy.position
        performance = self.strategy.get_performance_metrics()
        
        return {
            'analysis': analysis,
            'trade_executed': trade_result,
            'current_position': position,
            'performance': performance
        }
    
    def run(self, iterations: int = 10, interval: int = 60):
        """
        Run the trading bot for specified iterations
        
        Args:
            iterations: Number of iterations to run
            interval: Time between iterations (seconds)
        """
        if not self.model_trained:
            print("Training models first...")
            self.train_models()
        
        print(f"\nStarting trading bot for {iterations} iterations...")
        print(f"Symbol: {self.symbol}")
        print(f"Initial Capital: ${self.initial_capital:,.2f}\n")
        
        self.is_running = True
        
        for i in range(iterations):
            if not self.is_running:
                print("Bot stopped.")
                break
            
            print(f"\n{'='*60}")
            print(f"Iteration {i+1}/{iterations} - {datetime.now()}")
            print('='*60)
            
            try:
                result = self.run_iteration()
                
                # Display analysis
                analysis = result['analysis']
                print(f"\nPrice: ${analysis['current_price']:,.2f}")
                print(f"Price Signal: {analysis['price_signal']}")
                print(f"Sentiment Signal: {analysis['sentiment_signal']}")
                print(f"Combined Action: {analysis['combined_signal']['action']} "
                      f"(Confidence: {analysis['combined_signal']['confidence']:.2f})")
                
                # Display trade if executed
                if result['trade_executed']:
                    trade = result['trade_executed']
                    print(f"\n>>> TRADE EXECUTED <<<")
                    print(f"Action: {trade['action']} {trade.get('side', '')}")
                    print(f"Price: ${trade['price']:,.2f}")
                    if 'pnl' in trade:
                        print(f"PnL: ${trade['pnl']:,.2f} ({trade['pnl_pct']:.2f}%)")
                
                # Display position
                if result['current_position']:
                    pos = result['current_position']
                    print(f"\n>>> CURRENT POSITION <<<")
                    print(f"Side: {pos['side']}")
                    print(f"Amount: {pos['amount']:.4f}")
                    print(f"Entry: ${pos['entry_price']:,.2f}")
                    print(f"Stop Loss: ${pos['stop_loss']:,.2f}")
                    print(f"Take Profit: ${pos['take_profit']:,.2f}")
                
                # Display performance
                perf = result['performance']
                print(f"\n>>> PERFORMANCE <<<")
                print(f"Capital: ${perf['current_capital']:,.2f}")
                print(f"Total Return: ${perf['total_return']:,.2f} ({perf['total_return_pct']:.2f}%)")
                print(f"Total Trades: {perf['total_trades']}")
                print(f"Win Rate: {perf['win_rate']:.2f}%")
                
            except Exception as e:
                print(f"Error in iteration: {e}")
                import traceback
                traceback.print_exc()
            
            # Wait for next iteration
            if i < iterations - 1:
                print(f"\nWaiting {interval} seconds until next iteration...")
                time.sleep(interval)
        
        print(f"\n{'='*60}")
        print("Trading bot completed!")
        print('='*60)
        
        # Final performance summary
        final_performance = self.strategy.get_performance_metrics()
        print(f"\nFINAL PERFORMANCE SUMMARY")
        print(f"Initial Capital: ${self.initial_capital:,.2f}")
        print(f"Final Capital: ${final_performance['current_capital']:,.2f}")
        print(f"Total Return: ${final_performance['total_return']:,.2f}")
        print(f"Return %: {final_performance['total_return_pct']:.2f}%")
        print(f"Total Trades: {final_performance['total_trades']}")
        print(f"Winning Trades: {final_performance['winning_trades']}")
        print(f"Losing Trades: {final_performance['losing_trades']}")
        print(f"Win Rate: {final_performance['win_rate']:.2f}%")
        
        self.is_running = False
        
        return final_performance
    
    def stop(self):
        """Stop the trading bot"""
        self.is_running = False
        print("Stopping trading bot...")
    
    def get_status(self) -> Dict:
        """
        Get current bot status
        
        Returns:
            Dictionary with bot status
        """
        return {
            'is_running': self.is_running,
            'model_trained': self.model_trained,
            'symbol': self.symbol,
            'current_capital': self.strategy.current_capital,
            'position': self.strategy.position,
            'performance': self.strategy.get_performance_metrics()
        }


if __name__ == "__main__":
    # Example usage
    print("Initializing Cryptocurrency Trading Bot...")
    
    bot = CryptoTradingBot(
        symbol='BTC/USDT',
        initial_capital=10000,
        timeframe='1h',
        lookback=60
    )
    
    # Train models
    bot.train_models(historical_periods=500)
    
    # Run bot for a few iterations
    final_performance = bot.run(iterations=5, interval=10)
    
    print("\nBot execution completed!")
