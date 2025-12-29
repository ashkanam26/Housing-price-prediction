# Quick Start Guide - Crypto Trading Bot

## 🚀 Quick Installation & Run

### Option 1: Quick Start Script (Easiest)

```bash
# Install dependencies
pip install -r requirements-crypto-bot.txt

# Run the bot
python run_crypto_bot.py
```

Follow the prompts to configure and run the bot!

### Option 2: Jupyter Notebook Demo

```bash
# Install dependencies
pip install -r requirements-crypto-bot.txt

# Launch Jupyter
jupyter notebook crypto_bot_demo.ipynb
```

Run all cells to see a complete demonstration.

### Option 3: Web Interface

```bash
# Install dependencies
pip install -r requirements-crypto-bot.txt

# Start the web server
cd crypto_bot/web
python app.py

# Open browser to http://localhost:5000
```

Use the interactive dashboard to control the bot!

### Option 4: Python Script

```python
from crypto_bot.bot import CryptoTradingBot

# Initialize
bot = CryptoTradingBot(
    symbol='BTC/USDT',
    initial_capital=10000,
    timeframe='1h'
)

# Train models
bot.train_models(historical_periods=500)

# Run bot
bot.run(iterations=10, interval=60)
```

## 📋 What's Included

### Core Components

1. **Data Fetcher** (`crypto_bot/data/fetcher.py`)
   - Fetches OHLCV data (simulated by default)
   - Adds technical indicators (RSI, MACD, Bollinger Bands, etc.)

2. **Price Predictor** (`crypto_bot/models/price_predictor.py`)
   - ML model for price prediction
   - Uses Gradient Boosting (can be extended to LSTM/GRU)
   - Generates BUY/SELL/HOLD signals

3. **Sentiment Analyzer** (`crypto_bot/models/sentiment_analyzer.py`)
   - NLP-based sentiment analysis
   - Crypto-specific lexicon
   - Analyzes news/social media text

4. **Trading Strategy** (`crypto_bot/strategies/ml_strategy.py`)
   - Combines ML predictions, sentiment, and technical analysis
   - Risk management (stop-loss, take-profit)
   - Position sizing

5. **Main Bot** (`crypto_bot/bot.py`)
   - Orchestrates all components
   - Manages trading iterations
   - Tracks performance

6. **Web Interface** (`crypto_bot/web/`)
   - Flask backend API
   - Interactive dashboard
   - Real-time monitoring
   - Chart visualization

## 📊 Features

### ML/DL Models
- ✅ Price prediction using Gradient Boosting
- ✅ Technical indicator integration
- ✅ Model training and persistence
- 🔄 Extensible to LSTM/GRU networks

### NLP Sentiment Analysis
- ✅ Text sentiment classification
- ✅ Market sentiment aggregation
- ✅ Trading signal generation
- 🔄 Can integrate with Twitter/news APIs

### Trading Features
- ✅ Multi-signal combination (price + sentiment + technical)
- ✅ Risk management (stop-loss, take-profit)
- ✅ Position sizing based on risk
- ✅ Performance tracking
- ✅ Trade history

### Web Interface
- ✅ Real-time dashboard
- ✅ Interactive controls
- ✅ Price charts
- ✅ Performance metrics
- ✅ Activity logs

## 🎯 Usage Examples

### Example 1: Basic Usage

```python
from crypto_bot.bot import CryptoTradingBot

bot = CryptoTradingBot(symbol='BTC/USDT', initial_capital=10000)
bot.train_models()
bot.run(iterations=5, interval=60)
```

### Example 2: Custom Configuration

```python
from crypto_bot.bot import CryptoTradingBot
from crypto_bot.strategies.ml_strategy import TradingStrategy

bot = CryptoTradingBot(symbol='ETH/USDT', initial_capital=5000)
bot.strategy = TradingStrategy(
    initial_capital=5000,
    risk_per_trade=0.01,  # 1% risk
    stop_loss_pct=0.02,   # 2% stop loss
    take_profit_pct=0.05  # 5% take profit
)

bot.train_models(historical_periods=1000)
bot.run(iterations=20, interval=30)
```

### Example 3: Analysis Only

```python
from crypto_bot.bot import CryptoTradingBot

bot = CryptoTradingBot(symbol='BTC/USDT', initial_capital=10000)
bot.train_models()

# Just analyze, don't trade
analysis = bot.analyze_market()
print(f"Current Price: ${analysis['current_price']}")
print(f"Signal: {analysis['combined_signal']['action']}")
print(f"Confidence: {analysis['combined_signal']['confidence']}")
```

### Example 4: Web Interface

1. Start server: `cd crypto_bot/web && python app.py`
2. Open browser: `http://localhost:5000`
3. Click "Initialize" to set up bot
4. Click "Train Models" to train ML models
5. Click "Start Trading" to begin
6. Monitor performance in real-time

## 📈 Understanding the Signals

The bot combines three types of signals:

1. **Price Prediction (40% weight)**: ML model predicts future price
   - BUY: Price expected to increase
   - SELL: Price expected to decrease
   - HOLD: No clear direction

2. **Sentiment Analysis (30% weight)**: NLP analyzes market sentiment
   - BUY: Bullish sentiment
   - SELL: Bearish sentiment
   - HOLD: Neutral sentiment

3. **Technical Indicators (30% weight)**: RSI, MACD, Moving Averages
   - BUY: Oversold, bullish crossovers
   - SELL: Overbought, bearish crossovers
   - HOLD: No clear signals

**Combined Signal**: Weighted average with confidence score
- Only trades when confidence > 60%

## 🛡️ Risk Management

The bot includes several risk management features:

- **Position Sizing**: Calculates optimal size based on risk
- **Stop Loss**: Exits at specified loss level (default 3%)
- **Take Profit**: Exits at specified profit level (default 6%)
- **Risk per Trade**: Limits risk to 2% of capital per trade
- **Confidence Filter**: Only trades high-confidence signals

## 🔧 Configuration

### Bot Parameters
- `symbol`: Trading pair (e.g., 'BTC/USDT')
- `initial_capital`: Starting capital (e.g., 10000)
- `timeframe`: Candle timeframe ('1m', '1h', '1d')
- `lookback`: Periods for prediction (e.g., 60)

### Strategy Parameters
- `risk_per_trade`: Max risk per trade (default: 0.02 = 2%)
- `stop_loss_pct`: Stop loss % (default: 0.03 = 3%)
- `take_profit_pct`: Take profit % (default: 0.06 = 6%)

## ⚠️ Important Notes

1. **Educational Purpose**: This is for learning and demonstration
2. **Simulated Data**: Uses simulated data by default
3. **No Real Trading**: Does not connect to real exchanges by default
4. **Test First**: Always test thoroughly before considering real trading
5. **Risk Warning**: Cryptocurrency trading is extremely risky

## 🔄 Extending the Bot

### Connect to Real Exchange

Install `ccxt`:
```bash
pip install ccxt
```

Modify `crypto_bot/data/fetcher.py`:
```python
import ccxt

exchange = ccxt.binance()
ohlcv = exchange.fetch_ohlcv('BTC/USDT', '1h')
```

### Use Deep Learning Models

Install TensorFlow:
```bash
pip install tensorflow
```

Modify `crypto_bot/models/price_predictor.py` to use LSTM/GRU.

### Add Real Sentiment Data

Install Twitter API:
```bash
pip install tweepy
```

Fetch real tweets in `crypto_bot/models/sentiment_analyzer.py`.

## 📞 Support

For questions or issues:
- Email: ashkanam6731@gmail.com
- GitHub: Open an issue in the repository

## 🙏 Disclaimer

**This software is provided for educational purposes only.**

- DO NOT use real money without extensive testing
- The author is not responsible for any financial losses
- Cryptocurrency trading is highly risky
- Past performance does not guarantee future results
- Always do your own research (DYOR)

---

**Happy Learning! 🚀📚**
