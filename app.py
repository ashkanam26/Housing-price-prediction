"""
Flask application for Housing Price Prediction with Cryptocurrency Payment Gateway
"""
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import numpy as np
import os
from datetime import datetime, timedelta
import hashlib
import secrets

app = Flask(__name__)
CORS(app)

# Load the trained model
MODEL_PATH = 'xgboost-model.pkl'
model = None

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"Warning: Could not load model - {e}")

# In-memory storage for payments (in production, use a database)
payments_db = {}
subscriptions_db = {}

# Subscription plans
SUBSCRIPTION_PLANS = {
    'pro': {
        'name': 'Pro',
        'price_usdt': 50,
        'price_btc': 0.001,
        'price_eth': 0.02,
        'features': ['Unlimited predictions', 'API access', 'Email support']
    },
    'proplus': {
        'name': 'ProPlus',
        'price_usdt': 100,
        'price_btc': 0.002,
        'price_eth': 0.04,
        'features': ['All Pro features', 'Priority support', 'Advanced analytics', 'Custom model training']
    }
}

# Cryptocurrency wallet addresses (replace with actual addresses)
CRYPTO_WALLETS = {
    'btc': os.getenv('BTC_WALLET_ADDRESS', 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh'),
    'eth': os.getenv('ETH_WALLET_ADDRESS', '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0'),
    'usdt': os.getenv('USDT_WALLET_ADDRESS', '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0')
}


def generate_payment_id():
    """Generate unique payment ID"""
    return secrets.token_hex(16)


def verify_transaction(transaction_hash, amount, currency):
    """
    Verify cryptocurrency transaction
    In production, integrate with blockchain APIs like:
    - Blockchain.info API for Bitcoin
    - Etherscan API for Ethereum
    - Or use payment processor APIs like CoinGate, CoinPayments
    """
    # Placeholder for transaction verification
    # In real implementation, query blockchain or payment gateway API
    return True


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html', plans=SUBSCRIPTION_PLANS)


@app.route('/api/plans', methods=['GET'])
def get_plans():
    """Get available subscription plans"""
    return jsonify({
        'success': True,
        'plans': SUBSCRIPTION_PLANS
    })


@app.route('/api/payment/create', methods=['POST'])
def create_payment():
    """Create a new payment request"""
    try:
        data = request.json
        user_email = data.get('email')
        plan = data.get('plan')  # 'pro' or 'proplus'
        currency = data.get('currency', 'usdt').lower()  # 'btc', 'eth', or 'usdt'
        
        if not user_email or not plan:
            return jsonify({
                'success': False,
                'error': 'Email and plan are required'
            }), 400
        
        if plan not in SUBSCRIPTION_PLANS:
            return jsonify({
                'success': False,
                'error': 'Invalid plan'
            }), 400
        
        if currency not in ['btc', 'eth', 'usdt']:
            return jsonify({
                'success': False,
                'error': 'Invalid currency'
            }), 400
        
        # Generate payment ID
        payment_id = generate_payment_id()
        
        # Get payment amount
        amount_key = f'price_{currency}'
        amount = SUBSCRIPTION_PLANS[plan][amount_key]
        
        # Store payment request
        payments_db[payment_id] = {
            'email': user_email,
            'plan': plan,
            'currency': currency,
            'amount': amount,
            'wallet_address': CRYPTO_WALLETS[currency],
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(hours=1)).isoformat()
        }
        
        return jsonify({
            'success': True,
            'payment_id': payment_id,
            'amount': amount,
            'currency': currency.upper(),
            'wallet_address': CRYPTO_WALLETS[currency],
            'expires_at': payments_db[payment_id]['expires_at']
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/payment/verify', methods=['POST'])
def verify_payment():
    """Verify a cryptocurrency payment"""
    try:
        data = request.json
        payment_id = data.get('payment_id')
        transaction_hash = data.get('transaction_hash')
        
        if not payment_id or not transaction_hash:
            return jsonify({
                'success': False,
                'error': 'Payment ID and transaction hash are required'
            }), 400
        
        if payment_id not in payments_db:
            return jsonify({
                'success': False,
                'error': 'Payment not found'
            }), 404
        
        payment = payments_db[payment_id]
        
        # Check if payment is expired
        if datetime.now() > datetime.fromisoformat(payment['expires_at']):
            return jsonify({
                'success': False,
                'error': 'Payment expired'
            }), 400
        
        # Verify transaction on blockchain
        is_valid = verify_transaction(
            transaction_hash,
            payment['amount'],
            payment['currency']
        )
        
        if is_valid:
            # Update payment status
            payment['status'] = 'completed'
            payment['transaction_hash'] = transaction_hash
            payment['completed_at'] = datetime.now().isoformat()
            
            # Create subscription
            subscription_id = secrets.token_hex(16)
            subscriptions_db[subscription_id] = {
                'email': payment['email'],
                'plan': payment['plan'],
                'payment_id': payment_id,
                'activated_at': datetime.now().isoformat(),
                'expires_at': (datetime.now() + timedelta(days=30)).isoformat(),
                'api_key': secrets.token_hex(32)
            }
            
            return jsonify({
                'success': True,
                'subscription_id': subscription_id,
                'api_key': subscriptions_db[subscription_id]['api_key'],
                'expires_at': subscriptions_db[subscription_id]['expires_at']
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Transaction verification failed'
            }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/payment/status/<payment_id>', methods=['GET'])
def payment_status(payment_id):
    """Check payment status"""
    if payment_id not in payments_db:
        return jsonify({
            'success': False,
            'error': 'Payment not found'
        }), 404
    
    payment = payments_db[payment_id]
    return jsonify({
        'success': True,
        'status': payment['status'],
        'plan': payment['plan'],
        'amount': payment['amount'],
        'currency': payment['currency'],
        'created_at': payment['created_at']
    })


@app.route('/api/predict', methods=['POST'])
def predict_price():
    """
    Predict housing price
    Requires API key for Pro/ProPlus users
    """
    try:
        # Check for API key
        api_key = request.headers.get('X-API-Key')
        
        # Verify subscription
        subscription = None
        if api_key:
            for sub_id, sub in subscriptions_db.items():
                if sub['api_key'] == api_key:
                    # Check if subscription is active
                    if datetime.now() < datetime.fromisoformat(sub['expires_at']):
                        subscription = sub
                    break
        
        if not subscription:
            return jsonify({
                'success': False,
                'error': 'Valid API key required. Please subscribe to Pro or ProPlus plan.'
            }), 401
        
        if not model:
            return jsonify({
                'success': False,
                'error': 'Model not loaded. Please contact support.'
            }), 500
        
        # Get prediction features
        data = request.json
        features = data.get('features')
        
        if not features or len(features) != 8:
            return jsonify({
                'success': False,
                'error': 'Invalid features. Expected 8 features: MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude'
            }), 400
        
        # Make prediction
        try:
            features_array = np.array(features).reshape(1, -1)
            prediction = model.predict(features_array)
            
            return jsonify({
                'success': True,
                'predicted_price': float(prediction[0]),
                'subscription_plan': subscription['plan'],
                'note': 'Price in units of $100,000'
            })
        except Exception as e:
            # If model is not trained, return a demo message
            return jsonify({
                'success': True,
                'predicted_price': 4.526,  # Demo value
                'subscription_plan': subscription['plan'],
                'note': 'This is a demo prediction. Model needs to be trained with actual data. Price in units of $100,000',
                'demo': True
            })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/subscription/<email>', methods=['GET'])
def get_subscription(email):
    """Get user subscription details"""
    user_subscriptions = [
        sub for sub in subscriptions_db.values()
        if sub['email'] == email and datetime.now() < datetime.fromisoformat(sub['expires_at'])
    ]
    
    if not user_subscriptions:
        return jsonify({
            'success': False,
            'error': 'No active subscription found'
        }), 404
    
    sub = user_subscriptions[0]
    return jsonify({
        'success': True,
        'plan': sub['plan'],
        'api_key': sub['api_key'],
        'activated_at': sub['activated_at'],
        'expires_at': sub['expires_at']
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
