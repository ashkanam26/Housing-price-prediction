"""
Flask Web Application for Crypto Trading Bot
Provides web interface to control and monitor the bot
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime
import threading
import json
import os

# Import bot components
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crypto_bot.bot import CryptoTradingBot

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Global bot instance
bot = None
bot_thread = None
bot_config = {
    'symbol': 'BTC/USDT',
    'initial_capital': 10000,
    'timeframe': '1h',
    'lookback': 60,
    'interval': 60
}


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')


@app.route('/api/status')
def get_status():
    """Get bot status"""
    if bot is None:
        return jsonify({
            'status': 'not_initialized',
            'message': 'Bot not initialized'
        })
    
    status = bot.get_status()
    status['config'] = bot_config
    
    return jsonify(status)


@app.route('/api/initialize', methods=['POST'])
def initialize_bot():
    """Initialize the bot with configuration"""
    global bot, bot_config
    
    try:
        data = request.json
        
        # Update config
        if data:
            bot_config.update(data)
        
        # Create bot instance
        bot = CryptoTradingBot(
            symbol=bot_config['symbol'],
            initial_capital=bot_config['initial_capital'],
            timeframe=bot_config['timeframe'],
            lookback=bot_config['lookback']
        )
        
        return jsonify({
            'status': 'success',
            'message': 'Bot initialized successfully',
            'config': bot_config
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/train', methods=['POST'])
def train_models():
    """Train the ML models"""
    global bot
    
    if bot is None:
        return jsonify({
            'status': 'error',
            'message': 'Bot not initialized'
        }), 400
    
    try:
        data = request.json or {}
        periods = data.get('periods', 500)
        
        # Train in background thread
        def train_thread():
            bot.train_models(historical_periods=periods)
        
        thread = threading.Thread(target=train_thread)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'status': 'success',
            'message': 'Training started'
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/start', methods=['POST'])
def start_bot():
    """Start the trading bot"""
    global bot, bot_thread
    
    if bot is None:
        return jsonify({
            'status': 'error',
            'message': 'Bot not initialized'
        }), 400
    
    if not bot.model_trained:
        return jsonify({
            'status': 'error',
            'message': 'Models not trained. Train models first.'
        }), 400
    
    if bot.is_running:
        return jsonify({
            'status': 'error',
            'message': 'Bot already running'
        }), 400
    
    try:
        data = request.json or {}
        iterations = data.get('iterations', 100)
        interval = data.get('interval', bot_config['interval'])
        
        # Start bot in background thread
        def run_bot():
            bot.run(iterations=iterations, interval=interval)
        
        bot_thread = threading.Thread(target=run_bot)
        bot_thread.daemon = True
        bot_thread.start()
        
        return jsonify({
            'status': 'success',
            'message': 'Bot started'
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/stop', methods=['POST'])
def stop_bot():
    """Stop the trading bot"""
    global bot
    
    if bot is None:
        return jsonify({
            'status': 'error',
            'message': 'Bot not initialized'
        }), 400
    
    try:
        bot.stop()
        
        return jsonify({
            'status': 'success',
            'message': 'Bot stopped'
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/analysis')
def get_analysis():
    """Get current market analysis"""
    global bot
    
    if bot is None or not bot.model_trained:
        return jsonify({
            'status': 'error',
            'message': 'Bot not ready'
        }), 400
    
    try:
        analysis = bot.analyze_market()
        
        # Convert DataFrame to dict for JSON
        if 'dataframe' in analysis:
            df = analysis['dataframe'].tail(50)
            analysis['chart_data'] = {
                'timestamps': df['timestamp'].astype(str).tolist(),
                'prices': df['close'].tolist(),
                'volumes': df['volume'].tolist()
            }
            del analysis['dataframe']
        
        return jsonify(analysis)
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/performance')
def get_performance():
    """Get performance metrics"""
    global bot
    
    if bot is None:
        return jsonify({
            'status': 'error',
            'message': 'Bot not initialized'
        }), 400
    
    try:
        performance = bot.strategy.get_performance_metrics()
        trades = bot.strategy.trades_history
        
        return jsonify({
            'performance': performance,
            'trades': trades[-20:],  # Last 20 trades
            'equity_curve': bot.strategy.equity_curve
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/config', methods=['GET', 'POST'])
def config():
    """Get or update bot configuration"""
    global bot_config
    
    if request.method == 'GET':
        return jsonify(bot_config)
    
    else:  # POST
        try:
            data = request.json
            bot_config.update(data)
            
            return jsonify({
                'status': 'success',
                'config': bot_config
            })
        
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500


if __name__ == '__main__':
    print("Starting Crypto Trading Bot Web Interface...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
