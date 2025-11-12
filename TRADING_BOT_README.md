# Trading Bot AI - ربات ترید هوشمند رمز ارز

یک ربات ترید رمز ارز پیشرفته مبتنی بر هوش مصنوعی با قابلیت‌های ML، DL و NLP

An advanced AI-powered cryptocurrency trading bot with ML, DL, and NLP capabilities.

## 🚀 Features / ویژگی‌ها

### 1. Technical Analysis (تحلیل تکنیکال)
- **ML-based indicators**: استفاده از مدل‌های یادگیری ماشین برای تشخیص الگو
- **Classic indicators**: RSI, MACD, Bollinger Bands, Moving Averages, ATR
- **Pattern recognition**: تشخیص خودکار الگوهای قیمتی
- **Signal generation**: تولید سیگنال‌های خرید/فروش با اعتماد بالا

### 2. Fundamental Analysis (تحلیل بنیادی)
- **Market cap analysis**: تحلیل ارزش بازار
- **Volume analysis**: بررسی حجم معاملات
- **Liquidity assessment**: ارزیابی نقدینگی
- **Risk scoring**: امتیازدهی ریسک دارایی

### 3. Sentiment Analysis (تحلیل احساسات)
- **Social media monitoring**: پایش شبکه‌های اجتماعی (Twitter, Reddit)
- **NLP-based sentiment extraction**: استخراج احساسات با NLP
- **Fear & Greed Index**: شاخص ترس و طمع بازار
- **Influencer tracking**: ردیابی نظرات تأثیرگذاران

### 4. News Analysis (تحلیل اخبار)
- **Multi-source news aggregation**: جمع‌آوری اخبار از منابع مختلف
- **Event detection**: تشخیص رویدادهای مهم بازار
- **Impact assessment**: ارزیابی تأثیر اخبار
- **Trend identification**: شناسایی روندهای خبری

### 5. Risk Management (مدیریت ریسک)
- **AI-based risk assessment**: ارزیابی ریسک با هوش مصنوعی
- **Position sizing**: محاسبه اندازه پوزیشن بهینه
- **Stop loss calculation**: محاسبه حد ضرر هوشمند
- **Daily loss limits**: محدودیت ضرر روزانه
- **Maximum position limits**: محدودیت تعداد پوزیشن‌ها

### 6. Profit Management (مدیریت سود)
- **Trailing stop**: حد ضرر متحرک
- **Partial profit taking**: برداشت سود تدریجی
- **Multiple take-profit levels**: سطوح متعدد برداشت سود
- **Dynamic exit strategies**: استراتژی‌های خروج پویا

## 📁 Project Structure / ساختار پروژه

```
trading_bot_ai/
├── __init__.py                 # Package initialization
├── config.py                   # Configuration management
├── trading_bot.py             # Main trading bot orchestrator
├── analyzers/                 # Analysis modules
│   ├── technical_analyzer.py  # Technical analysis with ML
│   ├── fundamental_analyzer.py # Fundamental analysis
│   ├── sentiment_analyzer.py  # Sentiment analysis (NLP)
│   └── news_analyzer.py       # News analysis (NLP)
├── models/                    # AI models
│   ├── risk_manager.py        # AI-based risk management
│   └── profit_manager.py      # AI-based profit management
├── data_collectors/           # Data collection modules
│   ├── market_data_collector.py
│   ├── news_collector.py
│   └── sentiment_collector.py
└── utils/                     # Utility functions
```

## 🛠️ Installation / نصب

### Requirements / پیش‌نیازها

```bash
pip install -r requirments.txt
```

### Additional Dependencies for Production / وابستگی‌های اضافی برای محیط واقعی

برای استفاده در محیط واقعی، این کتابخانه‌ها را نیز نصب کنید:

```bash
# Exchange API integration
pip install ccxt

# Advanced NLP models
pip install transformers torch

# Deep Learning
pip install tensorflow  # or pytorch

# Social Media APIs
pip install tweepy praw

# News APIs
pip install newsapi-python
```

## 🚀 Quick Start / شروع سریع

### Basic Usage / استفاده پایه

```python
from trading_bot_ai import TradingBot

# Initialize the bot
bot = TradingBot()

# Run analysis for configured symbols
results = bot.run_analysis_cycle()

# Display results
for symbol, result in results.items():
    print(f"{symbol}: {result['decision']['decision']}")
    print(f"Confidence: {result['decision']['confidence']:.2%}")
```

### With Custom Configuration / با تنظیمات سفارشی

```python
from trading_bot_ai import TradingBot, Config

# Load custom configuration
bot = TradingBot(config_path='config_example.json')

# Analyze specific symbol
analysis = bot.analyze_symbol('BTC/USDT')

# Generate trading decision
decision = bot.generate_trading_decision(analysis)

# Execute trade (simulation)
if decision['decision'] != 'HOLD':
    result = bot.execute_trade(decision)
    print(f"Trade result: {result['status']}")
```

### Running the Example / اجرای مثال

```bash
python example_trading_bot.py
```

## ⚙️ Configuration / تنظیمات

فایل `config_example.json` را کپی کرده و بر اساس نیاز خود تغییر دهید:

```json
{
    "trading": {
        "symbols": ["BTC/USDT", "ETH/USDT"],
        "initial_capital": 10000,
        "max_position_size": 0.1
    },
    "risk_management": {
        "max_daily_loss": 0.05,
        "risk_per_trade": 0.02
    }
}
```

### Key Configuration Parameters / پارامترهای کلیدی

| Parameter | Description | Default |
|-----------|-------------|---------|
| `initial_capital` | سرمایه اولیه | 10000 |
| `max_position_size` | حداکثر اندازه پوزیشن (%) | 10% |
| `stop_loss_pct` | درصد حد ضرر | 2% |
| `take_profit_pct` | درصد حد سود | 5% |
| `max_daily_loss` | حداکثر ضرر روزانه | 5% |
| `risk_per_trade` | ریسک هر معامله | 2% |

## 📊 Analysis Workflow / گردش کار تحلیل

```
1. Data Collection (جمع‌آوری داده)
   ├─ Market Data (OHLCV, Order Book)
   ├─ News Data (اخبار)
   └─ Social Media Data (شبکه‌های اجتماعی)

2. Analysis (تحلیل)
   ├─ Technical Analysis (تحلیل تکنیکال)
   ├─ Fundamental Analysis (تحلیل بنیادی)
   ├─ Sentiment Analysis (تحلیل احساسات)
   └─ News Analysis (تحلیل اخبار)

3. Signal Generation (تولید سیگنال)
   └─ Weighted Decision (تصمیم وزن‌دار)

4. Risk Assessment (ارزیابی ریسک)
   └─ AI-based Risk Scoring (امتیازدهی ریسک)

5. Trade Execution (اجرای معامله)
   ├─ Position Sizing (تعیین اندازه پوزیشن)
   ├─ Stop Loss Calculation (محاسبه حد ضرر)
   └─ Take Profit Levels (سطوح برداشت سود)

6. Position Management (مدیریت پوزیشن)
   ├─ Trailing Stop (حد ضرر متحرک)
   └─ Profit Taking (برداشت سود)
```

## 🤖 AI Models / مدل‌های هوش مصنوعی

### Machine Learning Models
- **Random Forest**: تشخیص الگو و پیش‌بینی
- **XGBoost**: تحلیل پیشرفته داده‌های تکنیکال
- **Gradient Boosting**: بهبود دقت سیگنال‌ها

### Deep Learning Models (Optional)
- **LSTM**: پیش‌بینی سری‌های زمانی
- **Transformer**: تحلیل متن و احساسات
- **GRU**: مدل‌سازی ترندهای قیمتی

### NLP Models (Optional)
- **BERT**: تحلیل احساسات اخبار
- **RoBERTa**: تحلیل پیشرفته متون

## 📈 Signal Generation / تولید سیگنال

سیگنال نهایی بر اساس وزن‌دهی به تحلیل‌های مختلف محاسبه می‌شود:

- Technical Analysis: 35%
- Fundamental Analysis: 25%
- Sentiment Analysis: 20%
- News Analysis: 20%

### Signal Types / انواع سیگنال

- **BUY**: خرید (Weighted Score > 0.65)
- **HOLD**: نگهداری (0.35 ≤ Weighted Score ≤ 0.65)
- **SELL**: فروش (Weighted Score < 0.35)

## 🛡️ Risk Management Features / ویژگی‌های مدیریت ریسک

### Position Sizing / تعیین اندازه پوزیشن
```python
position_size = (capital × risk_per_trade) / price_risk
position_size = min(position_size, max_position_value / entry_price)
```

### Stop Loss Calculation / محاسبه حد ضرر
- ATR-based: استفاده از Average True Range
- Percentage-based: بر اساس درصد مشخص
- Support/Resistance: بر اساس سطوح حمایت/مقاومت

### Risk Scoring / امتیازدهی ریسک
- Volatility Risk: ریسک نوسانات
- Volume Risk: ریسک حجم پایین
- Sentiment Conflict: تناقض احساسات
- Trend Risk: ریسک خلاف جهت ترند

## 💰 Profit Management / مدیریت سود

### Trailing Stop / حد ضرر متحرک
به صورت خودکار با افزایش سود، حد ضرر به سمت بالا حرکت می‌کند.

### Partial Profit Taking / برداشت سود تدریجی
- سطح اول: برداشت 33% در سود 3%
- سطح دوم: برداشت 50% در سود 5%
- سطح سوم: برداشت 75% در سود 8%

## 📊 Example Output / نمونه خروجی

```
📊 Analysis Results for BTC/USDT
   Current Price: $50,000.00

   Technical Analysis:
   └─ Signal: BUY (Confidence: 75.00%)
      RSI: 45.23
      MACD: 125.50

   Fundamental Analysis:
   └─ Signal: BULLISH (Score: 78.00%)
      Risk Level: LOW

   Sentiment Analysis:
   └─ Signal: BUY (Score: 68.00%)
      Fear & Greed Index: 65/100
      Category: Greed

   News Analysis:
   └─ Signal: BUY
      Overall Sentiment: bullish
      Impact Level: medium

   🎯 FINAL DECISION: BUY
   Confidence: 72.50%
   Weighted Score: 71.25%

   Risk Assessment:
   └─ Risk Level: LOW
      Risk Score: 25.00%
      Recommendation: PROCEED
```

## 🔧 Customization / سفارشی‌سازی

### Adding Custom Indicators / افزودن اندیکاتورهای سفارشی

```python
# در فایل technical_analyzer.py
def calculate_custom_indicator(self, df):
    # محاسبه اندیکاتور سفارشی
    df['Custom_Indicator'] = ...
    return df
```

### Adjusting Signal Weights / تنظیم وزن سیگنال‌ها

```python
# در متد generate_trading_decision
weights = {
    'technical': 0.40,      # افزایش وزن تکنیکال
    'fundamental': 0.30,
    'sentiment': 0.15,
    'news': 0.15
}
```

## ⚠️ Important Notes / نکات مهم

### Simulation Mode / حالت شبیه‌سازی
⚠️ **توجه**: این نسخه در حالت شبیه‌سازی کار می‌کند و از داده‌های واقعی استفاده نمی‌کند.

برای استفاده در محیط واقعی:
1. اتصال به API صرافی (CCXT)
2. اتصال به API اخبار
3. اتصال به API شبکه‌های اجتماعی
4. پیاده‌سازی مدیریت سفارشات واقعی

### Risk Warning / هشدار ریسک
⚠️ **هشدار**: معاملات ارز دیجیتال ریسک بالایی دارد. این ربات ابزاری کمکی است و تضمینی برای سود ندارد.

- همیشه با سرمایه‌ای معامله کنید که توان از دست دادن آن را دارید
- قبل از استفاده واقعی، سیستم را به طور کامل تست کنید
- از تنظیمات مدیریت ریسک محافظت کنید

## 🤝 Contributing / مشارکت

برای بهبود این پروژه:
1. مشکلات و پیشنهادات خود را در Issues ثبت کنید
2. Pull Request ارسال کنید
3. مستندات را بهبود دهید

## 📝 License

این پروژه تحت لایسنس MIT منتشر شده است.

## 📧 Contact / تماس

برای سوالات و پشتیبانی: ashkanam6731@gmail.com

---

**Disclaimer**: This software is for educational purposes. Cryptocurrency trading involves substantial risk. Use at your own risk.

**سلب مسئولیت**: این نرم‌افزار برای اهداف آموزشی است. معاملات ارز دیجیتال ریسک قابل توجهی دارد. استفاده با مسئولیت خودتان است.
