# california housing price prediction + AI Trading Bot

## project overview
this repository contains two main projects:

1. **California Housing Price Prediction**: A machine learning model for predicting house prices in California
2. **AI-Powered Cryptocurrency Trading Bot**: An advanced trading bot with ML, DL, and NLP capabilities

---

## Project 1: California Housing Price Prediction

### goal
to build a predictive model for estimating house prices based on features such as median income, average rooms, population, and more.

## dataset
the dataset used is the **california housing dataset** from `scikit-learn`.

## models and results
 we evaluated three models and selected the best one:
1. **linear regression**
2. **random forest regressor**
3. **xgboost regressor (selected model)**

## visualizations

1. actual vs predicted values
    ![Actual vs predicted]
(https://github.com/ashkanam26/Housing-price-prediction/blob/main/actual_vs_predict.png)

2. feature importance
   ![feature importance]
(https://github.com/ashkanam26/Housing-price-prediction/blob/main/feature_importance.png)

3. housing price distribution
   ![housing price distribution]
(https://github.com/ashkanam26/Housing-price-prediction/blob/main/housing_price.png)

## how to run the project

1. clone this repository:
    ```bash git clone https://github.com/your-username/housing-price-prediction.git```
2. install the required packages from`requirements.txt`:
    ```bash pip install -r requirements.txt```
3. open the jupyter nootebook 
    `california housing price.ipynb` and run all cells.

## project files
- `california housing price.ipynb`:Main nootebook containing all steps for data analysis, model training, and evaluation.
- `XGBoost-model.pkl`:pre-trained xgboost model for predictions.
- `requirements.txt`: liat of required packages.
- `README.md`: project documentation.
- `actual-vs-predict.png`: actual vs predicted values plot.
- `feature-importance.png`: feature importance plot.
- `housing-price.png`: housing price distribution plot.

## tools and libraries

- python
- scikit-learn
- XGBoost
- matplotlib
- seaborn
- pandas
- Numpy
- joblib

## contact

for any questions,feel free to contact me at: [ashkanam6731@gmail.com]

---

## Project 2: AI-Powered Cryptocurrency Trading Bot

### 🚀 Overview
An advanced AI-powered cryptocurrency trading bot (ربات ترید رمز ارز) with comprehensive analysis capabilities:

- **Technical Analysis** (تحلیل تکنیکال): ML-based indicators, pattern recognition
- **Fundamental Analysis** (تحلیل بنیادی): Market cap, volume, liquidity analysis
- **Sentiment Analysis** (تحلیل احساسات): NLP-based social media monitoring
- **News Analysis** (تحلیل اخبار): Multi-source news aggregation and impact assessment
- **Risk Management** (مدیریت ریسک): AI-based position sizing and stop loss
- **Profit Management** (مدیریت سود): Trailing stops and partial profit taking

### 📁 Project Structure

```
trading_bot_ai/
├── analyzers/          # Technical, Fundamental, Sentiment, News analyzers
├── models/             # Risk Manager, Profit Manager
├── data_collectors/    # Market data, News, Sentiment collectors
└── trading_bot.py      # Main orchestrator
```

### 🛠️ Quick Start

```bash
# Run the example
python example_trading_bot.py
```

```python
from trading_bot_ai import TradingBot

# Initialize bot
bot = TradingBot()

# Run analysis
results = bot.run_analysis_cycle()

# Check status
status = bot.get_status()
```

### 📊 Features

- **Multi-Source Analysis**: Combines technical, fundamental, sentiment, and news analysis
- **AI Models**: Random Forest, XGBoost, and optional DL/NLP models
- **Risk Management**: Dynamic position sizing, stop loss, daily limits
- **Profit Optimization**: Trailing stops, partial profit taking
- **Comprehensive Reporting**: Detailed analysis and performance metrics

### 📖 Documentation

For detailed documentation, see [TRADING_BOT_README.md](TRADING_BOT_README.md)

### ⚠️ Important Note

This is a **simulation/educational version**. For production use:
- Connect to real exchange APIs (CCXT)
- Integrate news and social media APIs
- Implement actual order execution
- Add proper error handling and logging

### 🔧 Configuration

Copy `config_example.json` and customize:

```json
{
    "trading": {
        "symbols": ["BTC/USDT", "ETH/USDT"],
        "initial_capital": 10000
    },
    "risk_management": {
        "max_daily_loss": 0.05,
        "risk_per_trade": 0.02
    }
}
```

### 📈 Example Output

```
📊 Analysis Results for BTC/USDT
   Technical Analysis: BUY (Confidence: 75%)
   Fundamental Analysis: BULLISH (Score: 78%)
   Sentiment Analysis: BUY (Score: 68%)
   News Analysis: BUY (Impact: medium)
   
   🎯 FINAL DECISION: BUY
   Confidence: 72.50%
```

### 🤖 AI Models Used

- **ML**: Random Forest, XGBoost, Gradient Boosting
- **DL** (Optional): LSTM, Transformer, GRU
- **NLP** (Optional): BERT, RoBERTa for sentiment analysis

### 📝 License & Disclaimer

**License**: MIT

**⚠️ Risk Warning**: Cryptocurrency trading involves substantial risk of loss. This software is for educational purposes only. Use at your own risk. The authors are not responsible for any financial losses.

**سلب مسئولیت**: معاملات ارز دیجیتال ریسک بالایی دارد. این نرم‌افزار صرفاً جنبه آموزشی دارد و مسئولیت استفاده بر عهده کاربر است.

