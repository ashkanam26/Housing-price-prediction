"""
Example script demonstrating how to use the cryptocurrency payment API
"""
import requests
import time

BASE_URL = "http://localhost:5000"

def test_get_plans():
    """Test getting available subscription plans"""
    print("\n=== Testing Get Plans ===")
    response = requests.get(f"{BASE_URL}/api/plans")
    data = response.json()
    print("Plans:", data)
    return data['success']

def test_create_payment():
    """Test creating a payment request"""
    print("\n=== Testing Create Payment ===")
    payload = {
        "email": "test@example.com",
        "plan": "pro",
        "currency": "usdt"
    }
    response = requests.post(f"{BASE_URL}/api/payment/create", json=payload)
    data = response.json()
    print("Payment created:", data)
    
    if data['success']:
        print(f"\nPayment ID: {data['payment_id']}")
        print(f"Amount: {data['amount']} {data['currency']}")
        print(f"Wallet Address: {data['wallet_address']}")
        print(f"Expires at: {data['expires_at']}")
        return data['payment_id']
    return None

def test_payment_status(payment_id):
    """Test checking payment status"""
    print("\n=== Testing Payment Status ===")
    response = requests.get(f"{BASE_URL}/api/payment/status/{payment_id}")
    data = response.json()
    print("Payment status:", data)
    return data['success']

def test_verify_payment(payment_id):
    """Test verifying a payment"""
    print("\n=== Testing Verify Payment ===")
    # This is a test transaction hash - in real scenario, use actual blockchain transaction hash
    payload = {
        "payment_id": payment_id,
        "transaction_hash": "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    }
    response = requests.post(f"{BASE_URL}/api/payment/verify", json=payload)
    data = response.json()
    print("Payment verification:", data)
    
    if data['success']:
        print(f"\nSubscription ID: {data['subscription_id']}")
        print(f"API Key: {data['api_key']}")
        print(f"Expires at: {data['expires_at']}")
        return data['api_key']
    return None

def test_predict_price(api_key):
    """Test making a prediction with API key"""
    print("\n=== Testing Price Prediction ===")
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    # Example features for California Housing dataset
    payload = {
        "features": [
            8.3252,  # MedInc
            41.0,    # HouseAge
            6.98,    # AveRooms
            1.02,    # AveBedrms
            322.0,   # Population
            2.55,    # AveOccup
            37.88,   # Latitude
            -122.23  # Longitude
        ]
    }
    response = requests.post(f"{BASE_URL}/api/predict", headers=headers, json=payload)
    data = response.json()
    print("Prediction result:", data)
    
    if data['success']:
        print(f"\nPredicted Price: ${data['predicted_price'] * 100000:.2f}")
        print(f"Subscription Plan: {data['subscription_plan']}")
    return data['success']

def test_predict_without_api_key():
    """Test making a prediction without API key (should fail)"""
    print("\n=== Testing Prediction Without API Key ===")
    payload = {
        "features": [8.3252, 41.0, 6.98, 1.02, 322.0, 2.55, 37.88, -122.23]
    }
    response = requests.post(f"{BASE_URL}/api/predict", json=payload)
    data = response.json()
    print("Expected to fail:", data)
    return not data['success']  # Should fail without API key

def test_get_subscription():
    """Test getting subscription by email"""
    print("\n=== Testing Get Subscription ===")
    email = "test@example.com"
    response = requests.get(f"{BASE_URL}/api/subscription/{email}")
    data = response.json()
    print("Subscription info:", data)
    return data['success']

def run_all_tests():
    """Run all tests in sequence"""
    print("=" * 60)
    print("CRYPTOCURRENCY PAYMENT GATEWAY API TESTS")
    print("=" * 60)
    print("\nMake sure the Flask app is running on http://localhost:5000")
    print("Press Enter to continue...")
    input()
    
    try:
        # Test 1: Get plans
        assert test_get_plans(), "Get plans test failed"
        
        # Test 2: Create payment
        payment_id = test_create_payment()
        assert payment_id, "Create payment test failed"
        
        # Test 3: Check payment status
        assert test_payment_status(payment_id), "Payment status test failed"
        
        # Test 4: Verify payment and get API key
        api_key = test_verify_payment(payment_id)
        assert api_key, "Verify payment test failed"
        
        # Test 5: Make prediction with API key
        assert test_predict_price(api_key), "Prediction test failed"
        
        # Test 6: Try prediction without API key
        assert test_predict_without_api_key(), "Prediction without API key should fail"
        
        # Test 7: Get subscription by email
        assert test_get_subscription(), "Get subscription test failed"
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        
    except AssertionError as e:
        print("\n" + "=" * 60)
        print(f"❌ TEST FAILED: {e}")
        print("=" * 60)
    except requests.exceptions.ConnectionError:
        print("\n" + "=" * 60)
        print("❌ ERROR: Cannot connect to server")
        print("Make sure the Flask app is running on http://localhost:5000")
        print("Run: python app.py")
        print("=" * 60)
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ UNEXPECTED ERROR: {e}")
        print("=" * 60)

if __name__ == "__main__":
    run_all_tests()
