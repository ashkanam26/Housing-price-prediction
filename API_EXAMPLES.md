# API Usage Examples

This document provides practical examples of using the Cryptocurrency Payment Gateway API.

## Base URL

Development: `http://localhost:5000`
Production: Replace with your production URL

## Complete Payment Flow Example

### Step 1: Get Available Plans

```bash
curl -X GET http://localhost:5000/api/plans
```

Response:
```json
{
  "plans": {
    "pro": {
      "features": [
        "Unlimited predictions",
        "API access",
        "Email support"
      ],
      "name": "Pro",
      "price_btc": 0.001,
      "price_eth": 0.02,
      "price_usdt": 50
    },
    "proplus": {
      "features": [
        "All Pro features",
        "Priority support",
        "Advanced analytics",
        "Custom model training"
      ],
      "name": "ProPlus",
      "price_btc": 0.002,
      "price_eth": 0.04,
      "price_usdt": 100
    }
  },
  "success": true
}
```

### Step 2: Create Payment Request

```bash
curl -X POST http://localhost:5000/api/payment/create \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your@email.com",
    "plan": "pro",
    "currency": "usdt"
  }'
```

Response:
```json
{
  "amount": 50,
  "currency": "USDT",
  "expires_at": "2025-12-20T16:12:26.171730",
  "payment_id": "3a7db81cdba80c9bd337493bafafe36b",
  "success": true,
  "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0"
}
```

**Important:** 
- Send exactly the specified amount to the wallet address
- Complete the payment before expiry time (1 hour)
- Save the payment_id for verification

### Step 3: Send Cryptocurrency

Send the exact amount to the wallet address provided:
- For USDT: Send to the ERC-20 address
- For BTC: Send to the Bitcoin address
- For ETH: Send to the Ethereum address

After sending, copy your transaction hash from your wallet or block explorer.

### Step 4: Verify Payment

```bash
curl -X POST http://localhost:5000/api/payment/verify \
  -H "Content-Type: application/json" \
  -d '{
    "payment_id": "3a7db81cdba80c9bd337493bafafe36b",
    "transaction_hash": "0xYOUR_ACTUAL_TRANSACTION_HASH"
  }'
```

Response:
```json
{
  "api_key": "93f91dcf69584876e60f7d060375139b12bb84a10023dcb35366af40af1d88d6",
  "expires_at": "2026-01-19T15:12:26.234591",
  "subscription_id": "3023a5c0d36dd78c8b03350424240209",
  "success": true
}
```

**Save your API key!** You'll need it to access the prediction API.

### Step 5: Use the Prediction API

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "X-API-Key: YOUR_API_KEY_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "features": [
      8.3252,  
      41.0,    
      6.98,    
      1.02,    
      322.0,   
      2.55,    
      37.88,   
      -122.23  
    ]
  }'
```

Features in order:
1. MedInc (Median Income in $10,000s)
2. HouseAge (Median House Age)
3. AveRooms (Average Rooms per Household)
4. AveBedrms (Average Bedrooms per Household)
5. Population (Block Group Population)
6. AveOccup (Average Occupancy)
7. Latitude
8. Longitude

Response:
```json
{
  "predicted_price": 4.526,
  "subscription_plan": "pro",
  "success": true,
  "note": "Price in units of $100,000"
}
```

The predicted price is in units of $100,000, so 4.526 = $452,600

## Python Example

```python
import requests
import json

BASE_URL = "http://localhost:5000"

# Step 1: Create payment
payment_data = {
    "email": "user@example.com",
    "plan": "pro",
    "currency": "usdt"
}
response = requests.post(f"{BASE_URL}/api/payment/create", json=payment_data)
payment = response.json()
print(f"Payment ID: {payment['payment_id']}")
print(f"Send {payment['amount']} {payment['currency']} to: {payment['wallet_address']}")

# Step 2: After sending crypto, verify payment
payment_id = payment['payment_id']
tx_hash = input("Enter your transaction hash: ")

verify_data = {
    "payment_id": payment_id,
    "transaction_hash": tx_hash
}
response = requests.post(f"{BASE_URL}/api/payment/verify", json=verify_data)
result = response.json()
api_key = result['api_key']
print(f"API Key: {api_key}")

# Step 3: Make predictions
headers = {"X-API-Key": api_key}
prediction_data = {
    "features": [8.3252, 41.0, 6.98, 1.02, 322.0, 2.55, 37.88, -122.23]
}
response = requests.post(f"{BASE_URL}/api/predict", headers=headers, json=prediction_data)
prediction = response.json()
print(f"Predicted Price: ${prediction['predicted_price'] * 100000:.2f}")
```

## JavaScript Example

```javascript
const BASE_URL = 'http://localhost:5000';

// Step 1: Create payment
async function createPayment() {
  const response = await fetch(`${BASE_URL}/api/payment/create`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      email: 'user@example.com',
      plan: 'pro',
      currency: 'usdt'
    })
  });
  
  const payment = await response.json();
  console.log('Payment ID:', payment.payment_id);
  console.log(`Send ${payment.amount} ${payment.currency} to: ${payment.wallet_address}`);
  return payment.payment_id;
}

// Step 2: Verify payment
async function verifyPayment(paymentId, txHash) {
  const response = await fetch(`${BASE_URL}/api/payment/verify`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      payment_id: paymentId,
      transaction_hash: txHash
    })
  });
  
  const result = await response.json();
  console.log('API Key:', result.api_key);
  return result.api_key;
}

// Step 3: Make prediction
async function makePrediction(apiKey) {
  const response = await fetch(`${BASE_URL}/api/predict`, {
    method: 'POST',
    headers: {
      'X-API-Key': apiKey,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      features: [8.3252, 41.0, 6.98, 1.02, 322.0, 2.55, 37.88, -122.23]
    })
  });
  
  const prediction = await response.json();
  console.log('Predicted Price:', prediction.predicted_price * 100000);
  return prediction;
}

// Usage
(async () => {
  const paymentId = await createPayment();
  // User sends crypto and gets tx hash
  const txHash = '0xYOUR_TX_HASH';
  const apiKey = await verifyPayment(paymentId, txHash);
  const prediction = await makePrediction(apiKey);
})();
```

## Additional Endpoints

### Check Payment Status

```bash
curl -X GET http://localhost:5000/api/payment/status/{payment_id}
```

### Get User Subscription

```bash
curl -X GET http://localhost:5000/api/subscription/{email}
```

## Error Handling

All endpoints return JSON with a `success` field:

Success response:
```json
{
  "success": true,
  "data": {...}
}
```

Error response:
```json
{
  "success": false,
  "error": "Error message"
}
```

## Rate Limits

Currently no rate limits in development. In production, consider implementing:
- 100 requests per hour per API key
- 10 payment creation requests per hour per IP
- 5 payment verification attempts per payment ID

## Security Best Practices

1. **Never share your API key** - Treat it like a password
2. **Use HTTPS in production** - Never send API keys over HTTP
3. **Store API keys securely** - Use environment variables or secure vaults
4. **Rotate API keys regularly** - Implement key rotation for better security
5. **Verify transaction on blockchain** - Always check transaction confirmations

## Support

For API issues or questions:
- Email: ashkanam6731@gmail.com
- GitHub Issues: https://github.com/ashkanam26/Housing-price-prediction/issues
