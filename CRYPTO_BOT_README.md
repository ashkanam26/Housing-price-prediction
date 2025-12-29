# 🤖 Cryptocurrency Trading Bot with ML/DL/NLP

A comprehensive cryptocurrency trading bot that uses Machine Learning (ML), Deep Learning (DL), and Natural Language Processing (NLP) to make intelligent trading decisions.

## 🌟 Features

### Machine Learning & Deep Learning
- **Price Prediction Models**: Uses advanced ML algorithms (Gradient Boosting, can be extended to LSTM/GRU)
- **Technical Analysis**: Integrates RSI, MACD, Bollinger Bands, Moving Averages
- **Backtesting Framework**: Test strategies on historical data
- **Model Persistence**: Save and load trained models

### Natural Language Processing
- **Sentiment Analysis**: Analyzes market sentiment from news and social media
- **Crypto-Specific Lexicon**: Specialized vocabulary for cryptocurrency market
- **Multi-Source Analysis**: Combines sentiment from various text sources
- **Signal Generation**: Converts sentiment into actionable trading signals

### Trading Strategy
- **Multi-Signal Combination**: Combines price predictions, sentiment, and technical indicators
- **Risk Management**: Configurable stop-loss and take-profit levels
- **Position Sizing**: Intelligent position sizing based on risk
- **Performance Tracking**: Comprehensive metrics and trade history

### Web Interface
- **Real-Time Dashboard**: Monitor bot performance in real-time
- **Interactive Controls**: Start/stop bot, configure parameters
- **Live Charts**: Visualize price movements and indicators
- **Trade History**: View detailed trade logs and performance metrics
- **Responsive Design**: Works on desktop and mobile devices

## 📁 Project Structure

```
crypto_bot/
├── __init__.py              # Package initialization
├── bot.py                   # Main trading bot orchestrator
├── data/
│   ├── __init__.py
│   └── fetcher.py          # Data fetching and technical indicators
├── models/
│   ├── __init__.py
│   ├── price_predictor.py  # ML/DL price prediction model
│   └── sentiment_analyzer.py # NLP sentiment analysis
├── strategies/
│   ├── __init__.py
│   └── ml_strategy.py      # Trading strategy engine
├── utils/
│   └── __init__.py
└── web/
    ├── app.py              # Flask web application
    ├── templates/
    │   └── index.html      # Dashboard HTML
    └── static/
        ├── css/
        │   └── style.css   # Dashboard styles
        └── js/
            └── dashboard.js # Dashboard JavaScript
```

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/ashkanam26/Housing-price-prediction.git
cd Housing-price-prediction
```

2. **Install dependencies**:
```bash
pip install -r requirements-crypto-bot.txt
```

### Running the Bot (CLI)

```python
from crypto_bot.bot import CryptoTradingBot

# Initialize bot
bot = CryptoTradingBot(
    symbol='BTC/USDT',
    initial_capital=10000,
    timeframe='1h',
    lookback=60
)

# Train models
bot.train_models(historical_periods=500)

# Run bot
bot.run(iterations=10, interval=60)
```

### Running the Web Interface

1. **Start the web server**:
```bash
cd crypto_bot/web
python app.py
```

2. **Open browser**:
Navigate to `http://localhost:5000`

3. **Use the dashboard**:
   - Click "Initialize" to set up the bot
   - Click "Train Models" to train ML models
   - Click "Start Trading" to begin trading
   - Monitor performance in real-time

## 📊 Usage Examples

### Example 1: Quick Test Run

```python
from crypto_bot.bot import CryptoTradingBot

bot = CryptoTradingBot(symbol='BTC/USDT', initial_capital=10000)
bot.train_models()
performance = bot.run(iterations=5, interval=10)
print(f"Final Return: {performance['total_return_pct']:.2f}%")
```

### Example 2: Custom Configuration

```python
from crypto_bot.bot import CryptoTradingBot
from crypto_bot.strategies.ml_strategy import TradingStrategy

# Custom strategy settings
bot = CryptoTradingBot(symbol='ETH/USDT', initial_capital=5000)
bot.strategy = TradingStrategy(
    initial_capital=5000,
    risk_per_trade=0.01,  # 1% risk per trade
    stop_loss_pct=0.02,   # 2% stop loss
    take_profit_pct=0.05  # 5% take profit
)

bot.train_models(historical_periods=1000)
bot.run(iterations=20, interval=30)
```

### Example 3: Data Analysis

```python
from crypto_bot.data.fetcher import CryptoDataFetcher
import matplotlib.pyplot as plt

# Fetch and analyze data
fetcher = CryptoDataFetcher()
df = fetcher.fetch_ohlcv('BTC/USDT', '1h', 500)
df = fetcher.add_technical_indicators(df)

# Plot
plt.figure(figsize=(15, 8))
plt.plot(df['timestamp'], df['close'], label='Price')
plt.plot(df['timestamp'], df['sma_7'], label='SMA 7')
plt.plot(df['timestamp'], df['sma_25'], label='SMA 25')
plt.legend()
plt.show()
```

### Example 4: Sentiment Analysis

```python
from crypto_bot.models.sentiment_analyzer import SentimentAnalyzer

analyzer = SentimentAnalyzer()

texts = [
    "Bitcoin showing strong bullish momentum!",
    "Crypto market crash imminent, sell now!",
    "Ethereum upgrade successful, major adoption incoming"
]

sentiment = analyzer.get_market_sentiment(texts)
signal = analyzer.get_trading_signal(texts)

print(f"Overall Sentiment: {sentiment['overall_sentiment']}")
print(f"Trading Signal: {signal}")
```

## 🔧 Configuration

### Bot Parameters

- **symbol**: Trading pair (e.g., 'BTC/USDT', 'ETH/USDT')
- **initial_capital**: Starting capital in USDT
- **timeframe**: Candle timeframe ('1m', '5m', '1h', '1d', etc.)
- **lookback**: Number of periods for model training

### Strategy Parameters

- **risk_per_trade**: Maximum risk per trade (default: 2%)
- **stop_loss_pct**: Stop loss percentage (default: 3%)
- **take_profit_pct**: Take profit percentage (default: 6%)

### Model Parameters

- **lookback**: Number of past timesteps for prediction
- **prediction_horizon**: Steps ahead to predict
- **epochs**: Training epochs (default: 50)

## 📈 Performance Metrics

The bot tracks comprehensive performance metrics:

- **Total Return**: Absolute and percentage returns
- **Win Rate**: Percentage of profitable trades
- **Total Trades**: Number of executed trades
- **Average Win/Loss**: Average profit and loss per trade
- **Maximum Equity**: Peak portfolio value
- **Current Capital**: Real-time portfolio value

## 🎯 Trading Signals

The bot combines multiple signal sources:

1. **Price Prediction (40% weight)**: ML model predicts future price movement
2. **Sentiment Analysis (30% weight)**: NLP analyzes market sentiment
3. **Technical Indicators (30% weight)**: RSI, MACD, Moving Averages, Bollinger Bands

Signals are combined with confidence scoring to make final trading decisions.

## 🛡️ Risk Management

Built-in risk management features:

- **Position Sizing**: Calculates optimal position size based on risk
- **Stop Loss**: Automatic exit at specified loss level
- **Take Profit**: Automatic exit at specified profit level
- **Capital Protection**: Never risks more than available capital
- **Confidence Filtering**: Only trades high-confidence signals (>60%)

## 🔄 Extending the Bot

### Adding Real Exchange Connectivity

To connect to real exchanges, install `ccxt`:

```bash
pip install ccxt
```

Then modify `data/fetcher.py` to use real exchange APIs:

```python
import ccxt

exchange = ccxt.binance({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET'
})

# Fetch real data
ohlcv = exchange.fetch_ohlcv('BTC/USDT', '1h')
```

### Using Advanced Deep Learning

For LSTM/GRU models, install TensorFlow:

```bash
pip install tensorflow
```

Then modify `models/price_predictor.py` to use real neural networks.

### Adding Real Sentiment Data

Integrate Twitter API or news APIs:

```bash
pip install tweepy
```

Fetch real tweets and news for sentiment analysis.

## ⚠️ Disclaimer

**This is an educational project for learning purposes.**

- **DO NOT use real money without thorough testing**
- Cryptocurrency trading carries significant risk
- Past performance does not guarantee future results
- Always test strategies on paper trading first
- The bot uses simulated data by default
- Author is not responsible for financial losses

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, contact: ashkanam6731@gmail.com

## 🙏 Acknowledgments

- Built with Python, Flask, Chart.js
- Uses scikit-learn, XGBoost for ML
- Inspired by quantitative trading strategies

---

**Happy Trading! 🚀📈**
