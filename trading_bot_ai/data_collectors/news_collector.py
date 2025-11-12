"""
News Data Collection Module
"""

from typing import Dict, List
from datetime import datetime, timedelta
import random


class NewsCollector:
    """Collect cryptocurrency news from various sources"""
    
    def __init__(self, config: Dict):
        """
        Initialize news collector
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.news_config = config.get('news_analysis', {})
        self.sources = self.news_config.get('sources', ['cryptonews', 'coindesk', 'cointelegraph'])
        self.update_interval = self.news_config.get('update_interval', 300)
        
        # Cache
        self.news_cache = []
        self.last_fetch = None
    
    def fetch_latest_news(
        self,
        symbols: List[str] = None,
        limit: int = 50
    ) -> List[Dict]:
        """
        Fetch latest cryptocurrency news
        
        Args:
            symbols: List of symbols to filter news (optional)
            limit: Maximum number of news items
            
        Returns:
            List of news items
        """
        # Check cache
        if self.last_fetch and (datetime.now() - self.last_fetch).seconds < self.update_interval:
            return self.news_cache[:limit]
        
        # Simulate fetching news (in real implementation, use news APIs)
        news_items = self._simulate_news_data(symbols, limit)
        
        # Update cache
        self.news_cache = news_items
        self.last_fetch = datetime.now()
        
        return news_items
    
    def _simulate_news_data(
        self,
        symbols: List[str] = None,
        limit: int = 50
    ) -> List[Dict]:
        """
        Simulate news data for demonstration
        In production, this would fetch real news from APIs
        """
        news_templates = [
            {
                'type': 'positive',
                'titles': [
                    '{symbol} reaches new all-time high amid institutional adoption',
                    'Major partnership announced for {symbol} blockchain',
                    '{symbol} sees record trading volume as investors show confidence',
                    'Institutional investors increase {symbol} holdings',
                    'Bullish sentiment grows for {symbol} as fundamentals strengthen',
                    '{symbol} upgrade successfully completed, bringing new features',
                    'Major retailer announces {symbol} payment integration',
                    '{symbol} ETF approval moves closer to reality'
                ]
            },
            {
                'type': 'negative',
                'titles': [
                    'Regulatory concerns weigh on {symbol} price',
                    '{symbol} faces selling pressure as market sentiment turns bearish',
                    'Security researchers discover potential vulnerability in {symbol}',
                    '{symbol} trading halted temporarily due to technical issues',
                    'Market analysts warn of potential {symbol} correction',
                    'Large {symbol} holder moves funds to exchange, sparking sell-off fears',
                    'Regulatory body announces investigation into {symbol} activities',
                    '{symbol} experiences network congestion issues'
                ]
            },
            {
                'type': 'neutral',
                'titles': [
                    'Analysts provide mixed outlook for {symbol}',
                    '{symbol} consolidates as traders await next move',
                    'What to watch for {symbol} in the coming week',
                    '{symbol} technical analysis: Key levels to watch',
                    'Market update: {symbol} trading sideways',
                    '{symbol} community discusses future development roadmap',
                    'Expert panel debates {symbol} valuation',
                    'Deep dive: Understanding {symbol} tokenomics'
                ]
            }
        ]
        
        if not symbols:
            symbols = ['Bitcoin', 'Ethereum', 'Cryptocurrency']
        
        news_items = []
        
        for i in range(limit):
            # Random selection
            news_type = random.choice(news_templates)
            title_template = random.choice(news_type['titles'])
            symbol = random.choice(symbols).split('/')[0] if '/' in random.choice(symbols) else random.choice(symbols)
            
            title = title_template.format(symbol=symbol)
            
            # Generate publish time (within last 48 hours)
            hours_ago = random.uniform(0, 48)
            published_at = datetime.now() - timedelta(hours=hours_ago)
            
            # Generate content
            content = self._generate_news_content(title, news_type['type'])
            
            news_items.append({
                'id': f'news_{i}',
                'title': title,
                'content': content,
                'source': random.choice(self.sources),
                'published_at': published_at.isoformat(),
                'url': f'https://example.com/news/{i}',
                'category': news_type['type']
            })
        
        # Sort by publish time (newest first)
        news_items.sort(key=lambda x: x['published_at'], reverse=True)
        
        return news_items
    
    def _generate_news_content(self, title: str, sentiment_type: str) -> str:
        """Generate simulated news content"""
        positive_phrases = [
            'strong momentum', 'increased adoption', 'positive outlook',
            'bullish trend', 'institutional interest', 'record highs'
        ]
        
        negative_phrases = [
            'regulatory pressure', 'market uncertainty', 'selling pressure',
            'bearish sentiment', 'concerns raised', 'downward trend'
        ]
        
        neutral_phrases = [
            'market consolidation', 'mixed signals', 'sideways movement',
            'awaiting direction', 'technical levels', 'range-bound trading'
        ]
        
        if sentiment_type == 'positive':
            phrases = positive_phrases
        elif sentiment_type == 'negative':
            phrases = negative_phrases
        else:
            phrases = neutral_phrases
        
        content = f"{title}. Market analysts note {random.choice(phrases)} in recent trading activity. "
        content += f"Traders are observing {random.choice(phrases)} as the situation develops. "
        content += "Volume indicators show active participation from market participants."
        
        return content
    
    def fetch_news_by_source(self, source: str, limit: int = 20) -> List[Dict]:
        """
        Fetch news from a specific source
        
        Args:
            source: News source name
            limit: Maximum number of news items
            
        Returns:
            List of news items from the source
        """
        all_news = self.fetch_latest_news(limit=100)
        return [item for item in all_news if item['source'] == source][:limit]
    
    def fetch_news_by_timeframe(
        self,
        hours: int = 24,
        limit: int = 50
    ) -> List[Dict]:
        """
        Fetch news within a specific timeframe
        
        Args:
            hours: Number of hours to look back
            limit: Maximum number of news items
            
        Returns:
            List of recent news items
        """
        all_news = self.fetch_latest_news(limit=limit)
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        filtered_news = []
        for item in all_news:
            published_at = datetime.fromisoformat(item['published_at'])
            if published_at >= cutoff_time:
                filtered_news.append(item)
        
        return filtered_news
    
    def search_news(self, keywords: List[str], limit: int = 20) -> List[Dict]:
        """
        Search news by keywords
        
        Args:
            keywords: List of keywords to search
            limit: Maximum number of results
            
        Returns:
            List of matching news items
        """
        all_news = self.fetch_latest_news(limit=100)
        results = []
        
        for item in all_news:
            text = f"{item['title']} {item['content']}".lower()
            
            # Check if any keyword matches
            if any(keyword.lower() in text for keyword in keywords):
                results.append(item)
            
            if len(results) >= limit:
                break
        
        return results
    
    def get_news_summary(self, hours: int = 24) -> Dict[str, any]:
        """
        Get summary of news from the specified period
        
        Args:
            hours: Number of hours to analyze
            
        Returns:
            News summary statistics
        """
        news_items = self.fetch_news_by_timeframe(hours)
        
        # Count by source
        by_source = {}
        for item in news_items:
            source = item['source']
            by_source[source] = by_source.get(source, 0) + 1
        
        # Count by category
        by_category = {}
        for item in news_items:
            category = item.get('category', 'unknown')
            by_category[category] = by_category.get(category, 0) + 1
        
        return {
            'total_news': len(news_items),
            'timeframe_hours': hours,
            'by_source': by_source,
            'by_category': by_category,
            'latest_timestamp': news_items[0]['published_at'] if news_items else None
        }
