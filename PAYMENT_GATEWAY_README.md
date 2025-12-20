# 🏠 California Housing Price Prediction with Cryptocurrency Payment Gateway

## Project Overview
This project combines machine learning for California housing price prediction with a cryptocurrency payment gateway system. Users can subscribe to Pro or ProPlus plans using Bitcoin (BTC), Ethereum (ETH), or USDT (Tether) to access the prediction API.

## Features

### Machine Learning
- **XGBoost Model**: High-accuracy housing price predictions
- **8 Features**: MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude
- **Pre-trained Model**: Ready-to-use model included

### Payment Gateway
- **Multiple Cryptocurrencies**: Support for BTC, ETH, and USDT
- **Direct Payments**: Payments go directly to your wallet addresses
- **Two Subscription Plans**:
  - **Pro**: $50 USDT / 0.001 BTC / 0.02 ETH
    - Unlimited predictions
    - API access
    - Email support
  - **ProPlus**: $100 USDT / 0.002 BTC / 0.04 ETH
    - All Pro features
    - Priority support
    - Advanced analytics
    - Custom model training

### API Features
- RESTful API with authentication
- API key-based access control
- Subscription management
- Payment verification system

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/ashkanam26/Housing-price-prediction.git
cd Housing-price-prediction
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure wallet addresses**
```bash
cp .env.example .env
```

Edit `.env` file and add your actual cryptocurrency wallet addresses:
```
BTC_WALLET_ADDRESS=your_bitcoin_address
ETH_WALLET_ADDRESS=your_ethereum_address
USDT_WALLET_ADDRESS=your_usdt_address
```

4. **Run the application**
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

### Web Interface

1. **Visit** `http://localhost:5000`
2. **Select a plan** (Pro or ProPlus)
3. **Enter your email**
4. **Choose cryptocurrency** (BTC, ETH, or USDT)
5. **Create payment request**
6. **Send payment** to the provided wallet address
7. **Enter transaction hash** to verify payment
8. **Receive API key** for accessing the prediction API

### API Usage

Once you have your API key, you can make predictions:

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "features": [8.3252, 41.0, 6.98, 1.02, 322.0, 2.55, 37.88, -122.23]
  }'
```

Response:
```json
{
    "success": true,
    "predicted_price": 4.526,
    "subscription_plan": "pro"
}
```

## API Endpoints

### Payment Endpoints

#### Get Subscription Plans
```
GET /api/plans
```

#### Create Payment Request
```
POST /api/payment/create
Body: {
    "email": "user@example.com",
    "plan": "pro",
    "currency": "usdt"
}
```

#### Verify Payment
```
POST /api/payment/verify
Body: {
    "payment_id": "payment_id_here",
    "transaction_hash": "0x..."
}
```

#### Check Payment Status
```
GET /api/payment/status/{payment_id}
```

#### Get User Subscription
```
GET /api/subscription/{email}
```

### Prediction Endpoint

#### Predict Housing Price
```
POST /api/predict
Headers: X-API-Key: your_api_key
Body: {
    "features": [MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude]
}
```

## Feature Descriptions

The model requires 8 features for prediction:

1. **MedInc**: Median income in block group (in $10,000s)
2. **HouseAge**: Median house age in block group
3. **AveRooms**: Average number of rooms per household
4. **AveBedrms**: Average number of bedrooms per household
5. **Population**: Block group population
6. **AveOccup**: Average number of household members
7. **Latitude**: Block group latitude
8. **Longitude**: Block group longitude

## Security Notes

⚠️ **Important**: 
- Never commit your actual wallet addresses to public repositories
- Use environment variables for sensitive data
- In production, implement proper blockchain verification
- Consider using payment gateway services like CoinGate or CoinPayments for automatic verification
- Implement proper database for storing payments and subscriptions
- Add rate limiting and DDoS protection
- Use HTTPS in production

## Production Deployment

For production deployment, consider:

1. **Database**: Replace in-memory storage with PostgreSQL/MySQL
2. **Payment Verification**: Integrate with blockchain APIs:
   - Bitcoin: Blockchain.info API, BlockCypher
   - Ethereum: Etherscan API, Infura
   - Or use payment processors: CoinGate, CoinPayments, NOWPayments

3. **Security**:
   - Enable HTTPS
   - Add rate limiting
   - Implement proper authentication
   - Add input validation
   - Use environment variables for all secrets

4. **Monitoring**:
   - Add logging
   - Set up error tracking
   - Monitor payment transactions

## Integration with Payment Processors

For automatic payment verification, you can integrate with:

### CoinGate
```python
import coingate
client = coingate.Client('YOUR_API_KEY')
```

### CoinPayments
```python
from coinpayments import CoinPayments
client = CoinPayments(public_key, private_key)
```

### NOWPayments
```python
import requests
headers = {'x-api-key': 'YOUR_API_KEY'}
```

## Development

### Project Structure
```
Housing-price-prediction/
├── app.py                          # Main Flask application
├── templates/
│   └── index.html                  # Web interface
├── static/
│   ├── css/
│   │   └── style.css              # Styles
│   └── js/
│       └── main.js                # Frontend logic
├── xgboost-model.pkl              # Trained model
├── requirements.txt                # Python dependencies
├── .env.example                   # Environment variables template
└── README.md                      # This file
```

### Running Tests

```bash
# Test prediction API
curl -X POST http://localhost:5000/api/predict \
  -H "X-API-Key: test_key" \
  -H "Content-Type: application/json" \
  -d '{"features": [8.3252, 41.0, 6.98, 1.02, 322.0, 2.55, 37.88, -122.23]}'
```

## Troubleshooting

### Model Not Loading
- Ensure `xgboost-model.pkl` is in the root directory
- Check that all dependencies are installed

### Payment Not Verifying
- Check transaction hash is correct
- Ensure payment amount matches exactly
- Verify wallet address is correct

### API Key Not Working
- Check subscription is still active
- Ensure API key is included in headers
- Verify subscription was created successfully

## Changelog

### Version 1.0.0
- Initial release with cryptocurrency payment gateway
- Support for BTC, ETH, and USDT
- Pro and ProPlus subscription plans
- RESTful API for housing price predictions
- Web interface for easy payments

## Contact

For questions or support:
- Email: ashkanam6731@gmail.com
- GitHub: [@ashkanam26](https://github.com/ashkanam26)

## License

This project is licensed under the terms in the LICENSE file.

## Acknowledgments

- California Housing Dataset from scikit-learn
- XGBoost for the prediction model
- Flask for the web framework
