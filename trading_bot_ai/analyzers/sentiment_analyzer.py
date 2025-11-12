"""
Sentiment Analysis Module using NLP
"""

import re
import numpy as np
from typing import Dict, List
from collections import Counter


class SentimentAnalyzer:
    """Sentiment analysis using NLP for social media and news"""
    
    def __init__(self, config: Dict):
        """
        Initialize sentiment analyzer
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.enabled = config.get('sentiment_analysis', {}).get('enabled', True)
        self.sentiment_threshold = config.get('sentiment_analysis', {}).get('sentiment_threshold', 0.6)
        
        # Simple sentiment lexicon (can be replaced with transformer models)
        self.positive_words = {
            'bullish', 'moon', 'pump', 'buy', 'long', 'profit', 'gain', 'surge',
            'rally', 'breakout', 'strong', 'growth', 'up', 'rise', 'soar', 'rocket',
            'green', 'win', 'success', 'positive', 'optimistic', 'bull', 'calls'
        }
        
        self.negative_words = {
            'bearish', 'dump', 'sell', 'short', 'loss', 'crash', 'drop', 'fall',
            'decline', 'down', 'red', 'weak', 'fear', 'panic', 'correction', 'bear',
            'puts', 'collapse', 'plunge', 'tank', 'negative', 'pessimistic'
        }
    
    def analyze_text(self, text: str) -> Dict[str, any]:
        """
        Analyze sentiment of a single text
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment analysis results
        """
        if not self.enabled or not text:
            return {'sentiment': 'neutral', 'score': 0.5, 'confidence': 0.0}
        
        # Preprocess text
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        # Count sentiment words
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            return {'sentiment': 'neutral', 'score': 0.5, 'confidence': 0.0}
        
        # Calculate sentiment score
        sentiment_score = positive_count / total_sentiment_words
        
        # Determine sentiment
        if sentiment_score > 0.6:
            sentiment = 'positive'
        elif sentiment_score < 0.4:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        # Calculate confidence based on number of sentiment words
        confidence = min(total_sentiment_words / max(len(words), 1), 1.0)
        
        return {
            'sentiment': sentiment,
            'score': sentiment_score,
            'confidence': confidence,
            'positive_words': positive_count,
            'negative_words': negative_count
        }
    
    def analyze_batch(self, texts: List[str]) -> Dict[str, any]:
        """
        Analyze sentiment of multiple texts
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            Aggregated sentiment analysis
        """
        if not texts:
            return {
                'overall_sentiment': 'neutral',
                'sentiment_score': 0.5,
                'confidence': 0.0,
                'distribution': {'positive': 0, 'neutral': 0, 'negative': 0}
            }
        
        sentiments = []
        scores = []
        confidences = []
        
        for text in texts:
            result = self.analyze_text(text)
            sentiments.append(result['sentiment'])
            scores.append(result['score'])
            confidences.append(result['confidence'])
        
        # Calculate overall metrics
        avg_score = np.mean(scores)
        avg_confidence = np.mean(confidences)
        
        # Count sentiment distribution
        sentiment_counts = Counter(sentiments)
        total_count = len(sentiments)
        
        distribution = {
            'positive': sentiment_counts.get('positive', 0) / total_count,
            'neutral': sentiment_counts.get('neutral', 0) / total_count,
            'negative': sentiment_counts.get('negative', 0) / total_count
        }
        
        # Determine overall sentiment
        if avg_score > 0.6:
            overall_sentiment = 'positive'
        elif avg_score < 0.4:
            overall_sentiment = 'negative'
        else:
            overall_sentiment = 'neutral'
        
        return {
            'overall_sentiment': overall_sentiment,
            'sentiment_score': avg_score,
            'confidence': avg_confidence,
            'distribution': distribution,
            'total_analyzed': total_count
        }
    
    def analyze_social_media(self, posts: List[Dict]) -> Dict[str, any]:
        """
        Analyze social media posts sentiment
        
        Args:
            posts: List of social media posts (dict with 'text' and 'source' keys)
            
        Returns:
            Social media sentiment analysis
        """
        if not posts:
            return {
                'signal': 'NEUTRAL',
                'score': 0.5,
                'by_source': {}
            }
        
        # Analyze all posts
        texts = [post.get('text', '') for post in posts]
        overall_analysis = self.analyze_batch(texts)
        
        # Analyze by source
        by_source = {}
        sources = set(post.get('source', 'unknown') for post in posts)
        
        for source in sources:
            source_texts = [post.get('text', '') for post in posts if post.get('source') == source]
            source_analysis = self.analyze_batch(source_texts)
            by_source[source] = source_analysis
        
        # Generate trading signal
        score = overall_analysis['sentiment_score']
        confidence = overall_analysis['confidence']
        
        if score > self.sentiment_threshold and confidence > 0.5:
            signal = 'BUY'
        elif score < (1 - self.sentiment_threshold) and confidence > 0.5:
            signal = 'SELL'
        else:
            signal = 'HOLD'
        
        return {
            'signal': signal,
            'score': score,
            'confidence': confidence,
            'overall_sentiment': overall_analysis['overall_sentiment'],
            'distribution': overall_analysis['distribution'],
            'by_source': by_source,
            'total_posts': len(posts)
        }
    
    def get_sentiment_trend(self, historical_sentiments: List[float]) -> Dict[str, any]:
        """
        Analyze sentiment trend over time
        
        Args:
            historical_sentiments: List of sentiment scores over time
            
        Returns:
            Trend analysis
        """
        if len(historical_sentiments) < 2:
            return {'trend': 'insufficient_data', 'direction': 'unknown'}
        
        # Calculate trend
        recent = historical_sentiments[-5:]  # Last 5 data points
        older = historical_sentiments[-10:-5] if len(historical_sentiments) >= 10 else historical_sentiments[:-5]
        
        if not older:
            return {'trend': 'insufficient_data', 'direction': 'unknown'}
        
        recent_avg = np.mean(recent)
        older_avg = np.mean(older)
        
        change = recent_avg - older_avg
        
        if change > 0.1:
            trend = 'improving'
            direction = 'bullish'
        elif change < -0.1:
            trend = 'deteriorating'
            direction = 'bearish'
        else:
            trend = 'stable'
            direction = 'neutral'
        
        return {
            'trend': trend,
            'direction': direction,
            'change': change,
            'recent_avg': recent_avg,
            'older_avg': older_avg
        }
    
    def calculate_fear_greed_index(self, sentiment_data: Dict) -> Dict[str, any]:
        """
        Calculate a simplified fear and greed index
        
        Args:
            sentiment_data: Sentiment analysis data
            
        Returns:
            Fear and greed index
        """
        score = sentiment_data.get('sentiment_score', 0.5)
        
        # Scale to 0-100
        index = int(score * 100)
        
        # Categorize
        if index >= 75:
            category = 'Extreme Greed'
            recommendation = 'Consider taking profits or reducing exposure'
        elif index >= 60:
            category = 'Greed'
            recommendation = 'Market is optimistic, watch for reversal signals'
        elif index >= 40:
            category = 'Neutral'
            recommendation = 'Market sentiment is balanced'
        elif index >= 25:
            category = 'Fear'
            recommendation = 'Market is pessimistic, look for buying opportunities'
        else:
            category = 'Extreme Fear'
            recommendation = 'Strong selling pressure, potential buying opportunity'
        
        return {
            'index': index,
            'category': category,
            'recommendation': recommendation
        }
