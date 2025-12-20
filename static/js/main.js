let selectedPlan = null;
let currentPaymentId = null;
let expiryInterval = null;

function selectPlan(planId) {
    selectedPlan = planId;
    
    // Show payment section
    document.getElementById('paymentSection').style.display = 'block';
    
    // Scroll to payment section
    document.getElementById('paymentSection').scrollIntoView({ behavior: 'smooth' });
    
    // Update selected plan info
    const plans = {
        'pro': { name: 'Pro', price_usdt: 50, price_btc: 0.001, price_eth: 0.02 },
        'proplus': { name: 'ProPlus', price_usdt: 100, price_btc: 0.002, price_eth: 0.04 }
    };
    
    const plan = plans[planId];
    document.getElementById('selectedPlanInfo').innerHTML = `
        <h3>پلان انتخاب شده: ${plan.name}</h3>
        <p>قیمت: ${plan.price_usdt} USDT یا ${plan.price_btc} BTC یا ${plan.price_eth} ETH</p>
    `;
    
    // Update currency dropdown
    updateCurrencyDisplay();
}

function updateCurrencyDisplay() {
    const currency = document.getElementById('currency').value;
    const plans = {
        'pro': { name: 'Pro', price_usdt: 50, price_btc: 0.001, price_eth: 0.02 },
        'proplus': { name: 'ProPlus', price_usdt: 100, price_btc: 0.002, price_eth: 0.04 }
    };
    
    if (selectedPlan) {
        const plan = plans[selectedPlan];
        const amount = currency === 'usdt' ? plan.price_usdt : 
                      currency === 'btc' ? plan.price_btc : 
                      plan.price_eth;
        
        document.getElementById('selectedPlanInfo').innerHTML = `
            <h3>پلان انتخاب شده: ${plan.name}</h3>
            <p>قیمت: ${amount} ${currency.toUpperCase()}</p>
        `;
    }
}

// Update currency display when selection changes
document.addEventListener('DOMContentLoaded', function() {
    const currencySelect = document.getElementById('currency');
    if (currencySelect) {
        currencySelect.addEventListener('change', updateCurrencyDisplay);
    }
});

async function createPayment() {
    const email = document.getElementById('email').value;
    const currency = document.getElementById('currency').value;
    
    if (!email) {
        alert('لطفاً ایمیل خود را وارد کنید');
        return;
    }
    
    if (!selectedPlan) {
        alert('لطفاً ابتدا یک پلان انتخاب کنید');
        return;
    }
    
    try {
        const response = await fetch('/api/payment/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                plan: selectedPlan,
                currency: currency
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentPaymentId = data.payment_id;
            
            // Show payment details
            document.getElementById('paymentAmount').textContent = 
                `${data.amount} ${data.currency}`;
            document.getElementById('walletAddress').textContent = data.wallet_address;
            document.getElementById('paymentId').textContent = data.payment_id;
            
            // Show payment details section
            document.getElementById('paymentDetails').style.display = 'block';
            
            // Start expiry timer
            startExpiryTimer(data.expires_at);
            
            // Scroll to payment details
            document.getElementById('paymentDetails').scrollIntoView({ behavior: 'smooth' });
        } else {
            alert('خطا: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('خطا در ایجاد درخواست پرداخت');
    }
}

function startExpiryTimer(expiresAt) {
    const expiryDate = new Date(expiresAt);
    
    // Clear existing interval
    if (expiryInterval) {
        clearInterval(expiryInterval);
    }
    
    expiryInterval = setInterval(() => {
        const now = new Date();
        const diff = expiryDate - now;
        
        if (diff <= 0) {
            document.getElementById('expiryTimer').textContent = 'منقضی شده';
            clearInterval(expiryInterval);
            return;
        }
        
        const minutes = Math.floor(diff / 60000);
        const seconds = Math.floor((diff % 60000) / 1000);
        
        document.getElementById('expiryTimer').textContent = 
            `${minutes}:${seconds.toString().padStart(2, '0')}`;
    }, 1000);
}

async function verifyPayment() {
    const txHash = document.getElementById('txHash').value;
    
    if (!txHash) {
        alert('لطفاً هش تراکنش را وارد کنید');
        return;
    }
    
    if (!currentPaymentId) {
        alert('شناسه پرداخت یافت نشد');
        return;
    }
    
    try {
        const response = await fetch('/api/payment/verify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                payment_id: currentPaymentId,
                transaction_hash: txHash
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Clear expiry timer
            if (expiryInterval) {
                clearInterval(expiryInterval);
            }
            
            // Hide payment details
            document.getElementById('paymentDetails').style.display = 'none';
            
            // Show subscription result
            document.getElementById('apiKey').textContent = data.api_key;
            document.getElementById('subscriptionResult').style.display = 'block';
            
            // Scroll to result
            document.getElementById('subscriptionResult').scrollIntoView({ behavior: 'smooth' });
        } else {
            alert('خطا: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('خطا در تایید پرداخت');
    }
}

function copyWalletAddress() {
    const walletAddress = document.getElementById('walletAddress').textContent;
    navigator.clipboard.writeText(walletAddress).then(() => {
        alert('آدرس کیف پول کپی شد');
    }).catch(err => {
        console.error('Error copying:', err);
        alert('خطا در کپی کردن');
    });
}

function copyApiKey() {
    const apiKey = document.getElementById('apiKey').textContent;
    navigator.clipboard.writeText(apiKey).then(() => {
        alert('API Key کپی شد');
    }).catch(err => {
        console.error('Error copying:', err);
        alert('خطا در کپی کردن');
    });
}
