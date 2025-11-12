# Crypto Trading Bot Store - Web Application

## Overview
This is a web application for browsing and purchasing cryptocurrency trading bot accounts. The application showcases various trading bots with their features, performance metrics, and pricing.

## Features
- Browse available trading bot accounts
- View detailed information about each bot
- Responsive design for mobile and desktop
- REST API endpoints for programmatic access
- Clean and modern UI

## Installation

1. Install the required dependencies:
```bash
pip install -r requirments.txt
```

## Running the Application

1. Start the Flask development server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## Application Structure

```
.
├── app.py                      # Main Flask application
├── templates/
│   ├── index.html             # Homepage with bot listings
│   └── bot_details.html       # Detailed bot information page
└── static/
    └── css/
        └── style.css          # Styling for the application
```

## API Endpoints

### Get All Bots
```
GET /api/bots
```
Returns a JSON array of all available bot accounts.

### Get Specific Bot
```
GET /api/bot/<bot_id>
```
Returns JSON details for a specific bot account.

## Available Bots

The application currently features:
1. **Bitcoin Trader Pro** - Advanced Bitcoin trading bot
2. **Ethereum Master Bot** - Specialized Ethereum trading bot
3. **Multi-Coin Trader** - Multi-cryptocurrency trading bot
4. **DeFi Yield Farmer** - Automated DeFi yield farming bot

## Customization

To add or modify bot accounts, edit the `BOT_ACCOUNTS` list in `app.py`:

```python
BOT_ACCOUNTS = [
    {
        'id': 1,
        'name': 'Bot Name',
        'description': 'Bot description',
        'price': 299,
        'currency': 'USD',
        'features': ['Feature 1', 'Feature 2'],
        'performance': '85% success rate'
    },
    # Add more bots...
]
```

## Production Deployment

For production deployment:

1. Set `debug=False` in `app.py`
2. Use a production WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

3. Configure a reverse proxy (nginx/Apache) for better performance and security

## Technology Stack

- **Backend**: Flask 3.0.0
- **Frontend**: HTML5, CSS3
- **Template Engine**: Jinja2 (included with Flask)

## License

See LICENSE file in the repository.

## Disclaimer

This is a demonstration application. Trading cryptocurrencies carries significant risk. Always do your own research before making any investment decisions.
