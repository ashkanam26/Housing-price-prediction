"""
Sentiment Data Collection Module
"""

from typing import Dict, List
from datetime import datetime, timedelta
import random


class SentimentCollector:
    """Collect sentiment data from social media and forums"""
    
    def __init__(self, config: Dict):
        """
        Initialize sentiment collector
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.sentiment_config = config.get('sentiment_analysis', {})
        self.sources = self.sentiment_config.get('sources', ['twitter', 'reddit', 'news'])
        
        # Cache
        self.sentiment_cache = {}
        self.last_fetch = {}
    
    def fetch_social_media_posts(
        self,
        symbol: str,
        source: str = 'twitter',
        limit: int = 100
    ) -> List[Dict]:
        """
        Fetch social media posts about a cryptocurrency
        
        Args:
            symbol: Cryptocurrency symbol
            source: Social media source ('twitter', 'reddit', etc.)
            limit: Maximum number of posts
            
        Returns:
            List of social media posts
        """
        cache_key = f"{symbol}_{source}"
        
        # Check cache
        if cache_key in self.sentiment_cache:
            last_fetch = self.last_fetch.get(cache_key)
            if last_fetch and (datetime.now() - last_fetch).seconds < 300:
                return self.sentiment_cache[cache_key][:limit]
        
        # Simulate fetching posts (in real implementation, use social media APIs)
        posts = self._simulate_social_posts(symbol, source, limit)
        
        # Update cache
        self.sentiment_cache[cache_key] = posts
        self.last_fetch[cache_key] = datetime.now()
        
        return posts
    
    def _simulate_social_posts(
        self,
        symbol: str,
        source: str,
        limit: int
    ) -> List[Dict]:
        """
        Simulate social media posts for demonstration
        In production, this would fetch real data from social media APIs
        """
        base_symbol = symbol.split('/')[0] if '/' in symbol else symbol
        
        # Post templates by sentiment
        positive_templates = [
            f'{base_symbol} to the moon! 🚀',
            f'Bullish on {base_symbol}, great fundamentals',
            f'Just bought more {base_symbol}, feeling confident',
            f'{base_symbol} looking strong, breakout incoming',
            f'Long on {base_symbol}, this is going up',
            f'{base_symbol} is undervalued, buying opportunity',
            f'Positive news for {base_symbol}, bullish!',
            f'{base_symbol} chart looks amazing 📈'
        ]
        
        negative_templates = [
            f'Bearish on {base_symbol}, selling pressure increasing',
            f'{base_symbol} looking weak, might drop more',
            f'Sold my {base_symbol}, too risky now',
            f'{base_symbol} chart showing bearish signals',
            f'Short on {base_symbol}, downtrend continues',
            f'Concerned about {base_symbol} fundamentals',
            f'Red flags on {base_symbol}, be careful',
            f'{base_symbol} breaking down 📉'
        ]
        
        neutral_templates = [
            f'What do you think about {base_symbol}?',
            f'Analyzing {base_symbol} chart, mixed signals',
            f'{base_symbol} consolidating, waiting for direction',
            f'Anyone holding {base_symbol}? Thoughts?',
            f'Looking at {base_symbol} data',
            f'{base_symbol} technical analysis needed',
            f'Watching {base_symbol} closely',
            f'What are your {base_symbol} price targets?'
        ]
        
        posts = []
        
        # Generate posts with weighted sentiment distribution
        # Slightly positive bias for demonstration
        sentiment_weights = {'positive': 0.4, 'neutral': 0.35, 'negative': 0.25}
        
        for i in range(limit):
            # Select sentiment based on weights
            rand = random.random()
            if rand < sentiment_weights['positive']:
                sentiment = 'positive'
                text = random.choice(positive_templates)
            elif rand < sentiment_weights['positive'] + sentiment_weights['neutral']:
                sentiment = 'neutral'
                text = random.choice(neutral_templates)
            else:
                sentiment = 'negative'
                text = random.choice(negative_templates)
            
            # Generate post metadata
            hours_ago = random.uniform(0, 24)
            posted_at = datetime.now() - timedelta(hours=hours_ago)
            
            # Simulate engagement metrics
            likes = int(random.expovariate(0.1)) + 1
            retweets = int(random.expovariate(0.2)) if source == 'twitter' else 0
            comments = int(random.expovariate(0.3))
            
            posts.append({
                'id': f'{source}_{i}',
                'text': text,
                'source': source,
                'author': f'user_{random.randint(1000, 9999)}',
                'posted_at': posted_at.isoformat(),
                'sentiment': sentiment,  # Ground truth for simulation
                'engagement': {
                    'likes': likes,
                    'retweets': retweets,
                    'comments': comments
                },
                'reach': random.randint(100, 10000)
            })
        
        # Sort by post time (newest first)
        posts.sort(key=lambda x: x['posted_at'], reverse=True)
        
        return posts
    
    def fetch_sentiment_summary(
        self,
        symbol: str,
        timeframe_hours: int = 24
    ) -> Dict[str, any]:
        """
        Get sentiment summary for a symbol
        
        Args:
            symbol: Cryptocurrency symbol
            timeframe_hours: Hours to look back
            
        Returns:
            Sentiment summary
        """
        all_posts = []
        
        # Fetch from all sources
        for source in self.sources:
            posts = self.fetch_social_media_posts(symbol, source, limit=50)
            
            # Filter by timeframe
            cutoff_time = datetime.now() - timedelta(hours=timeframe_hours)
            filtered_posts = [
                post for post in posts
                if datetime.fromisoformat(post['posted_at']) >= cutoff_time
            ]
            
            all_posts.extend(filtered_posts)
        
        if not all_posts:
            return {
                'symbol': symbol,
                'timeframe_hours': timeframe_hours,
                'total_posts': 0,
                'sentiment_distribution': {},
                'average_sentiment': 0.5
            }
        
        # Calculate sentiment distribution
        sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}
        total_reach = 0
        
        for post in all_posts:
            sentiment_counts[post['sentiment']] += 1
            total_reach += post.get('reach', 0)
        
        total_posts = len(all_posts)
        
        # Calculate weighted sentiment score
        positive_pct = sentiment_counts['positive'] / total_posts
        negative_pct = sentiment_counts['negative'] / total_posts
        sentiment_score = (positive_pct + 0.5 * (sentiment_counts['neutral'] / total_posts))
        
        return {
            'symbol': symbol,
            'timeframe_hours': timeframe_hours,
            'total_posts': total_posts,
            'sentiment_distribution': {
                'positive': sentiment_counts['positive'],
                'neutral': sentiment_counts['neutral'],
                'negative': sentiment_counts['negative']
            },
            'sentiment_percentages': {
                'positive': positive_pct * 100,
                'neutral': (sentiment_counts['neutral'] / total_posts) * 100,
                'negative': negative_pct * 100
            },
            'sentiment_score': sentiment_score,
            'total_reach': total_reach,
            'average_engagement': sum(
                post['engagement']['likes'] + post['engagement'].get('retweets', 0) 
                for post in all_posts
            ) / total_posts
        }
    
    def get_trending_topics(self, limit: int = 10) -> List[Dict]:
        """
        Get trending cryptocurrency topics
        
        Args:
            limit: Maximum number of trending topics
            
        Returns:
            List of trending topics
        """
        # Simulate trending topics
        topics = [
            'Bitcoin', 'Ethereum', 'DeFi', 'NFT', 'Altcoin',
            'Blockchain', 'Crypto regulation', 'Web3', 'Metaverse',
            'Layer 2', 'Staking', 'Mining', 'Exchange', 'Wallet'
        ]
        
        trending = []
        
        for topic in random.sample(topics, min(limit, len(topics))):
            trending.append({
                'topic': topic,
                'mentions_24h': random.randint(1000, 50000),
                'sentiment_score': random.uniform(0.3, 0.8),
                'trend': random.choice(['rising', 'falling', 'stable'])
            })
        
        # Sort by mentions
        trending.sort(key=lambda x: x['mentions_24h'], reverse=True)
        
        return trending
    
    def get_influencer_sentiment(
        self,
        symbol: str,
        min_followers: int = 10000
    ) -> List[Dict]:
        """
        Get sentiment from influential accounts
        
        Args:
            symbol: Cryptocurrency symbol
            min_followers: Minimum follower count to be considered influencer
            
        Returns:
            List of influencer posts
        """
        all_posts = self.fetch_social_media_posts(symbol, 'twitter', limit=100)
        
        # Simulate influencer status
        influencer_posts = []
        
        for post in all_posts:
            followers = random.randint(1000, 100000)
            
            if followers >= min_followers:
                post['followers'] = followers
                post['influence_score'] = (followers / 1000) * (1 + post['engagement']['likes'] / 100)
                influencer_posts.append(post)
        
        # Sort by influence score
        influencer_posts.sort(key=lambda x: x.get('influence_score', 0), reverse=True)
        
        return influencer_posts[:10]  # Top 10 influential posts
    
    def compare_sentiment_across_symbols(
        self,
        symbols: List[str]
    ) -> List[Dict]:
        """
        Compare sentiment across multiple symbols
        
        Args:
            symbols: List of cryptocurrency symbols
            
        Returns:
            Comparative sentiment data
        """
        comparisons = []
        
        for symbol in symbols:
            summary = self.fetch_sentiment_summary(symbol, timeframe_hours=24)
            
            comparisons.append({
                'symbol': symbol,
                'sentiment_score': summary['sentiment_score'],
                'total_posts': summary['total_posts'],
                'positive_pct': summary['sentiment_percentages']['positive'],
                'total_reach': summary['total_reach']
            })
        
        # Sort by sentiment score
        comparisons.sort(key=lambda x: x['sentiment_score'], reverse=True)
        
        return comparisons
