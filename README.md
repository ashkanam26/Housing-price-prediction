# california housing price prediction

## project overview
this project focuses on predicting house prices in california using machine learning model and includes a cryptocurrency payment gateway for monetization.

## 🆕 NEW: Cryptocurrency Payment Gateway

This project now includes a complete cryptocurrency payment system! Users can subscribe to Pro or ProPlus plans using Bitcoin, Ethereum, or USDT to access the housing price prediction API.

### Features
- **Multiple Cryptocurrencies**: BTC, ETH, USDT support
- **Direct Payments**: Payments go directly to your wallet
- **Two Subscription Tiers**: Pro ($50) and ProPlus ($100)
- **Secure API Access**: API key-based authentication
- **Web Interface**: Beautiful Persian/English UI for easy payments

### Quick Start

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure wallet addresses**
```bash
cp .env.example .env
# Edit .env with your actual wallet addresses
```

3. **Run the application**
```bash
python app.py
```

4. **Access the application**
```
http://localhost:5000
```

### Documentation
- [Payment Gateway README](PAYMENT_GATEWAY_README.md) - Complete documentation
- [API Examples](API_EXAMPLES.md) - Code examples and usage
- [Deployment Guide](DEPLOYMENT.md) - Production deployment instructions

---

## Original Project: Housing Price Prediction

## goal
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

