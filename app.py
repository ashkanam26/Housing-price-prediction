"""
Cryptocurrency Trading Bot Account Store
A simple web application for selling crypto trading bot accounts
"""

from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

# Sample bot accounts data
BOT_ACCOUNTS = [
    {
        'id': 1,
        'name': 'Bitcoin Trader Pro',
        'description': 'Advanced Bitcoin trading bot with ML algorithms',
        'price': 299,
        'currency': 'USD',
        'features': ['Auto-trading', 'Risk management', 'Real-time analytics'],
        'performance': '85% success rate'
    },
    {
        'id': 2,
        'name': 'Ethereum Master Bot',
        'description': 'Specialized Ethereum trading bot with smart contract integration',
        'price': 399,
        'currency': 'USD',
        'features': ['Smart contract trading', 'Gas optimization', 'Portfolio management'],
        'performance': '82% success rate'
    },
    {
        'id': 3,
        'name': 'Multi-Coin Trader',
        'description': 'Trade multiple cryptocurrencies simultaneously',
        'price': 499,
        'currency': 'USD',
        'features': ['Multi-exchange support', 'Arbitrage detection', 'Auto-rebalancing'],
        'performance': '88% success rate'
    },
    {
        'id': 4,
        'name': 'DeFi Yield Farmer',
        'description': 'Automated DeFi yield farming bot',
        'price': 599,
        'currency': 'USD',
        'features': ['Yield optimization', 'Gas-efficient', 'APY tracking'],
        'performance': '90% success rate'
    }
]

@app.route('/')
def index():
    """Homepage showing all available bot accounts"""
    return render_template('index.html', bots=BOT_ACCOUNTS)

@app.route('/bot/<int:bot_id>')
def bot_details(bot_id):
    """Detailed view of a specific bot account"""
    bot = next((bot for bot in BOT_ACCOUNTS if bot['id'] == bot_id), None)
    if bot:
        return render_template('bot_details.html', bot=bot)
    return "Bot not found", 404

@app.route('/api/bots')
def api_bots():
    """API endpoint to get all bot accounts"""
    return jsonify(BOT_ACCOUNTS)

@app.route('/api/bot/<int:bot_id>')
def api_bot(bot_id):
    """API endpoint to get specific bot account"""
    bot = next((bot for bot in BOT_ACCOUNTS if bot['id'] == bot_id), None)
    if bot:
        return jsonify(bot)
    return jsonify({'error': 'Bot not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
