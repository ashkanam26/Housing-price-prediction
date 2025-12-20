# درگاه پرداخت ارز دیجیتال - راهنمای فارسی

## معرفی

این پروژه یک درگاه پرداخت ارز دیجیتال کامل برای دریافت پول از کاربران است که می‌خواهند به سرویس پیش‌بینی قیمت مسکن با هوش مصنوعی دسترسی داشته باشند.

## ویژگی‌ها

### ارزهای دیجیتال پشتیبانی شده
- **بیت کوین (BTC)**
- **اتریوم (ETH)**
- **تتر (USDT)**

### پلان‌های اشتراک

#### پلان Pro - ۵۰ دلار
- پیش‌بینی‌های نامحدود
- دسترسی به API
- پشتیبانی ایمیلی

#### پلان ProPlus - ۱۰۰ دلار
- تمام امکانات Pro
- پشتیبانی اولویت‌دار
- تحلیل‌های پیشرفته
- آموزش مدل سفارشی

## نصب و راه‌اندازی

### ۱. نصب وابستگی‌ها
```bash
pip install -r requirements.txt
```

### ۲. تنظیم آدرس کیف پول‌ها
```bash
cp .env.example .env
```

فایل `.env` را باز کنید و آدرس کیف پول‌های خود را وارد کنید:

```
BTC_WALLET_ADDRESS=آدرس_کیف_پول_بیت_کوین_شما
ETH_WALLET_ADDRESS=آدرس_کیف_پول_اتریوم_شما
USDT_WALLET_ADDRESS=آدرس_کیف_پول_تتر_شما
```

### ۳. اجرای برنامه
```bash
python app.py
```

### ۴. باز کردن مرورگر
به آدرس زیر بروید:
```
http://localhost:5000
```

## نحوه استفاده

### برای کاربران (از طریق وب)

1. **انتخاب پلان**: یکی از پلان‌های Pro یا ProPlus را انتخاب کنید
2. **وارد کردن ایمیل**: ایمیل خود را وارد کنید
3. **انتخاب ارز**: بیت کوین، اتریوم یا تتر را انتخاب کنید
4. **ایجاد درخواست پرداخت**: دکمه ایجاد درخواست را بزنید
5. **ارسال ارز**: مبلغ مشخص شده را به آدرس نمایش داده شده ارسال کنید
6. **وارد کردن هش تراکنش**: پس از ارسال، هش تراکنش را وارد کنید
7. **دریافت API Key**: کلید API خود را دریافت و ذخیره کنید

### برای توسعه‌دهندگان (استفاده از API)

```python
import requests

# ۱. ایجاد درخواست پرداخت
response = requests.post('http://localhost:5000/api/payment/create', json={
    'email': 'your@email.com',
    'plan': 'pro',
    'currency': 'usdt'
})
payment = response.json()
print(f"آدرس پرداخت: {payment['wallet_address']}")
print(f"مبلغ: {payment['amount']} {payment['currency']}")

# ۲. تایید پرداخت
response = requests.post('http://localhost:5000/api/payment/verify', json={
    'payment_id': payment['payment_id'],
    'transaction_hash': 'هش_تراکنش_شما'
})
result = response.json()
api_key = result['api_key']

# ۳. استفاده از API برای پیش‌بینی
response = requests.post('http://localhost:5000/api/predict',
    headers={'X-API-Key': api_key},
    json={'features': [8.3252, 41.0, 6.98, 1.02, 322.0, 2.55, 37.88, -122.23]}
)
prediction = response.json()
print(f"قیمت پیش‌بینی شده: ${prediction['predicted_price'] * 100000:.2f}")
```

## نکات مهم امنیتی

⚠️ **توجه:**

1. **هرگز کلید API خود را با کسی به اشتراک نگذارید**
2. **آدرس کیف پول‌های واقعی خود را در فایل `.env` قرار دهید**
3. **در محیط واقعی حتماً از HTTPS استفاده کنید**
4. **برای تایید تراکنش‌ها از API بلاکچین استفاده کنید**
5. **از دیتابیس برای ذخیره اطلاعات پرداخت‌ها استفاده کنید**

## استقرار در محیط واقعی (Production)

برای استقرار در محیط واقعی، باید:

### ۱. از دیتابیس استفاده کنید
به جای ذخیره‌سازی در حافظه، از PostgreSQL یا MySQL استفاده کنید.

### ۲. تایید خودکار تراکنش‌ها
از سرویس‌های زیر برای تایید خودکار تراکنش‌ها استفاده کنید:
- **CoinGate**
- **CoinPayments**
- **NOWPayments**
- **Blockchain.info API** (برای بیت کوین)
- **Etherscan API** (برای اتریوم)

### ۳. امنیت
- HTTPS فعال کنید
- Rate Limiting اضافه کنید
- احراز هویت قوی پیاده‌سازی کنید
- ورودی‌ها را اعتبارسنجی کنید
- لاگ‌گذاری کامل داشته باشید

## ساختار فایل‌ها

```
Housing-price-prediction/
├── app.py                          # برنامه اصلی Flask
├── templates/
│   └── index.html                  # رابط کاربری وب
├── static/
│   ├── css/
│   │   └── style.css              # استایل‌ها
│   └── js/
│       └── main.js                # منطق فرانت‌اند
├── xgboost-model.pkl              # مدل آموزش دیده
├── requirements.txt                # وابستگی‌های Python
├── .env.example                   # الگوی متغیرهای محیطی
├── README.md                      # مستندات اصلی
├── PAYMENT_GATEWAY_README.md      # مستندات درگاه پرداخت
├── API_EXAMPLES.md                # مثال‌های استفاده از API
└── DEPLOYMENT.md                  # راهنمای استقرار
```

## API Endpoints

### دریافت پلان‌ها
```
GET /api/plans
```

### ایجاد درخواست پرداخت
```
POST /api/payment/create
Body: {"email": "...", "plan": "pro", "currency": "usdt"}
```

### تایید پرداخت
```
POST /api/payment/verify
Body: {"payment_id": "...", "transaction_hash": "..."}
```

### بررسی وضعیت پرداخت
```
GET /api/payment/status/{payment_id}
```

### دریافت اشتراک کاربر
```
GET /api/subscription/{email}
```

### پیش‌بینی قیمت مسکن
```
POST /api/predict
Headers: X-API-Key: your_api_key
Body: {"features": [...]}
```

## پشتیبانی

برای سوالات و مشکلات:
- ایمیل: ashkanam6731@gmail.com
- گیتهاب: [@ashkanam26](https://github.com/ashkanam26)

## مجوز

این پروژه تحت شرایط مندرج در فایل LICENSE منتشر شده است.

## تشکر

- از scikit-learn برای دیتاست California Housing
- از XGBoost برای مدل پیش‌بینی
- از Flask برای فریمورک وب
