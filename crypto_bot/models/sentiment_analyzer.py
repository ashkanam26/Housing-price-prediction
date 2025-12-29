"""
NLP Sentiment Analysis for Cryptocurrency
Analyzes news, social media, and other text data for market sentiment
"""

import pandas as pd
import numpy as np
from datetime import datetime
import re
from typing import List, Dict
import warnings
warnings.filterwarnings('ignore')


class SentimentAnalyzer:
    """
    Sentiment analysis for cryptocurrency market
    Analyzes text from news, tweets, and other sources
    """
    
    def __init__(self):
        """Initialize sentiment analyzer"""
        # Cryptocurrency-specific sentiment lexicon
        self.positive_words = {
            'bullish', 'moon', 'pump', 'rally', 'surge', 'breakout', 
            'adoption', 'partnership', 'upgrade', 'innovation', 'growth',
            'profit', 'gain', 'rise', 'up', 'high', 'bull', 'buy',
            'accumulate', 'hodl', 'strong', 'breakthrough', 'success'
        }
        
        self.negative_words = {
            'bearish', 'dump', 'crash', 'drop', 'fall', 'decline',
            'scam', 'hack', 'theft', 'regulation', 'ban', 'panic',
            'loss', 'down', 'low', 'bear', 'sell', 'fear', 'weak',
            'failure', 'concern', 'risk', 'volatile', 'uncertain'
        }
        
        self.neutral_words = {
            'stable', 'consolidation', 'sideways', 'range', 'analysis',
            'update', 'news', 'announcement', 'report', 'data'
        }
        
    def clean_text(self, text: str) -> str:
        """
        Clean and preprocess text
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        
        # Remove mentions and hashtags symbols but keep the words
        text = re.sub(r'[@#]', '', text)
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def analyze_text(self, text: str) -> Dict:
        """
        Analyze sentiment of a single text
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with sentiment scores and label
        """
        cleaned_text = self.clean_text(text)
        words = cleaned_text.split()
        
        # Count sentiment words
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        neutral_count = sum(1 for word in words if word in self.neutral_words)
        
        total_sentiment_words = positive_count + negative_count + neutral_count
        
        if total_sentiment_words == 0:
            sentiment_score = 0
            sentiment_label = 'neutral'
        else:
            # Calculate compound score (-1 to 1)
            sentiment_score = (positive_count - negative_count) / max(len(words), 1)
            
            # Determine label
            if sentiment_score > 0.05:
                sentiment_label = 'positive'
            elif sentiment_score < -0.05:
                sentiment_label = 'negative'
            else:
                sentiment_label = 'neutral'
        
        return {
            'text': text,
            'cleaned_text': cleaned_text,
            'sentiment_score': sentiment_score,
            'sentiment_label': sentiment_label,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'confidence': abs(sentiment_score)
        }
    
    def analyze_batch(self, texts: List[str]) -> pd.DataFrame:
        """
        Analyze sentiment for multiple texts
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            DataFrame with sentiment analysis results
        """
        results = []
        
        for text in texts:
            result = self.analyze_text(text)
            results.append(result)
        
        df = pd.DataFrame(results)
        return df
    
    def get_market_sentiment(self, texts: List[str]) -> Dict:
        """
        Get overall market sentiment from multiple sources
        
        Args:
            texts: List of texts (news, tweets, etc.)
            
        Returns:
            Dictionary with aggregated sentiment metrics
        """
        df = self.analyze_batch(texts)
        
        # Calculate aggregated metrics
        avg_sentiment = df['sentiment_score'].mean()
        sentiment_std = df['sentiment_score'].std()
        
        # Count sentiment categories
        sentiment_counts = df['sentiment_label'].value_counts().to_dict()
        
        # Determine overall sentiment
        if avg_sentiment > 0.05:
            overall_sentiment = 'BULLISH'
        elif avg_sentiment < -0.05:
            overall_sentiment = 'BEARISH'
        else:
            overall_sentiment = 'NEUTRAL'
        
        # Calculate strength (0-100)
        strength = min(abs(avg_sentiment) * 100, 100)
        
        return {
            'overall_sentiment': overall_sentiment,
            'avg_sentiment_score': avg_sentiment,
            'sentiment_std': sentiment_std,
            'strength': strength,
            'positive_count': sentiment_counts.get('positive', 0),
            'negative_count': sentiment_counts.get('negative', 0),
            'neutral_count': sentiment_counts.get('neutral', 0),
            'total_texts': len(texts),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_trading_signal(self, texts: List[str], 
                          threshold: float = 0.1) -> str:
        """
        Get trading signal based on sentiment
        
        Args:
            texts: List of texts to analyze
            threshold: Minimum sentiment score for signal
            
        Returns:
            'BUY', 'SELL', or 'HOLD'
        """
        sentiment = self.get_market_sentiment(texts)
        score = sentiment['avg_sentiment_score']
        
        if score > threshold and sentiment['strength'] > 20:
            return 'BUY'
        elif score < -threshold and sentiment['strength'] > 20:
            return 'SELL'
        else:
            return 'HOLD'
    
    def generate_sample_texts(self, sentiment_type: str = 'mixed', 
                            count: int = 10) -> List[str]:
        """
        Generate sample texts for demonstration
        
        Args:
            sentiment_type: 'positive', 'negative', or 'mixed'
            count: Number of texts to generate
            
        Returns:
            List of sample texts
        """
        positive_samples = [
            "Bitcoin is showing strong bullish momentum with new all-time highs!",
            "Ethereum upgrade successful, major adoption incoming! #bullish",
            "Crypto market rally continues as institutional investors accumulate more",
            "Breaking: Major tech company announces Bitcoin integration! Moon soon!",
            "Strong support levels holding, expecting another pump #cryptocurrency",
            "Positive regulatory news boosts market sentiment significantly",
            "Bitcoin breaks resistance, bulls in control! HODL strong",
            "Altcoins showing impressive gains across the board today",
            "Crypto adoption reaching new heights with mainstream partnerships",
            "Technical analysis suggests strong upward trend continuation"
        ]
        
        negative_samples = [
            "Bitcoin crash imminent as bearish patterns emerge #crypto",
            "Major exchange hack reported, market in panic sell mode",
            "Regulatory concerns weighing heavily on cryptocurrency prices",
            "Whale dump triggers massive price drop across crypto markets",
            "Bitcoin falls below key support level, bears taking control",
            "Negative news from regulators causing widespread fear in market",
            "Market sentiment turns bearish as prices continue to decline",
            "Crypto winter concerns grow as trading volumes drop significantly",
            "Technical indicators showing strong bearish divergence #bitcoin",
            "Risk of further downside as market uncertainty increases"
        ]
        
        neutral_samples = [
            "Bitcoin price consolidating in tight range awaiting breakout",
            "Crypto market showing mixed signals in sideways movement",
            "Analysis: Market remains range-bound with low volatility today",
            "Trading volume steady as prices stabilize after recent moves",
            "Cryptocurrency markets in consolidation phase according to analysts",
            "Bitcoin holding current levels as traders await next catalyst",
            "Market update: Stable prices across major cryptocurrencies today",
            "Crypto markets quiet ahead of important economic data release",
            "Technical analysis shows neutral momentum in short term outlook",
            "Sideways price action continues as market seeks direction"
        ]
        
        if sentiment_type == 'positive':
            return positive_samples[:count]
        elif sentiment_type == 'negative':
            return negative_samples[:count]
        else:  # mixed
            import random
            all_samples = positive_samples + negative_samples + neutral_samples
            random.shuffle(all_samples)
            return all_samples[:count]


if __name__ == "__main__":
    # Example usage
    analyzer = SentimentAnalyzer()
    
    # Generate sample texts
    texts = analyzer.generate_sample_texts('mixed', 20)
    
    print("Analyzing market sentiment...\n")
    
    # Analyze individual text
    result = analyzer.analyze_text(texts[0])
    print(f"Sample text: {result['text']}")
    print(f"Sentiment: {result['sentiment_label']} (score: {result['sentiment_score']:.3f})\n")
    
    # Get overall market sentiment
    market_sentiment = analyzer.get_market_sentiment(texts)
    print("Overall Market Sentiment:")
    print(f"  Sentiment: {market_sentiment['overall_sentiment']}")
    print(f"  Score: {market_sentiment['avg_sentiment_score']:.3f}")
    print(f"  Strength: {market_sentiment['strength']:.1f}%")
    print(f"  Positive: {market_sentiment['positive_count']}")
    print(f"  Negative: {market_sentiment['negative_count']}")
    print(f"  Neutral: {market_sentiment['neutral_count']}")
    
    # Get trading signal
    signal = analyzer.get_trading_signal(texts)
    print(f"\nTrading Signal: {signal}")
