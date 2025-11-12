"""
Simple tests for the Crypto Trading Bot Store application
"""

import unittest
from app import app, BOT_ACCOUNTS


class TestCryptoTradingBotStore(unittest.TestCase):
    """Test cases for the web application"""

    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True

    def test_homepage_loads(self):
        """Test that the homepage loads successfully"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Crypto Trading Bot Store', response.data)

    def test_api_bots_endpoint(self):
        """Test that the API endpoint returns bot data"""
        response = self.app.get('/api/bots')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 4)
        self.assertEqual(data[0]['name'], 'Bitcoin Trader Pro')

    def test_api_single_bot_endpoint(self):
        """Test that the API endpoint returns a specific bot"""
        response = self.app.get('/api/bot/1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['name'], 'Bitcoin Trader Pro')
        self.assertEqual(data['price'], 299)

    def test_bot_details_page(self):
        """Test that bot details page loads"""
        response = self.app.get('/bot/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bitcoin Trader Pro', response.data)

    def test_bot_not_found(self):
        """Test that non-existent bot returns 404"""
        response = self.app.get('/bot/999')
        self.assertEqual(response.status_code, 404)

    def test_api_bot_not_found(self):
        """Test that non-existent bot API returns 404"""
        response = self.app.get('/api/bot/999')
        self.assertEqual(response.status_code, 404)

    def test_bot_accounts_data(self):
        """Test that bot accounts have required fields"""
        for bot in BOT_ACCOUNTS:
            self.assertIn('id', bot)
            self.assertIn('name', bot)
            self.assertIn('description', bot)
            self.assertIn('price', bot)
            self.assertIn('features', bot)
            self.assertIn('performance', bot)


if __name__ == '__main__':
    unittest.main()
