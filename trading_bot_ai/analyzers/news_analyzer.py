"""
News Analysis Module using NLP
"""

import re
from typing import Dict, List
from datetime import datetime, timedelta
from collections import defaultdict


class NewsAnalyzer:
    """News analysis using NLP for cryptocurrency market news"""
    
    def __init__(self, config: Dict):
        """
        Initialize news analyzer
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.enabled = config.get('news_analysis', {}).get('enabled', True)
        self.sources = config.get('news_analysis', {}).get('sources', [])
        
        # Keywords for different categories
        self.bullish_keywords = {
            'adoption', 'partnership', 'integration', 'launch', 'upgrade', 'institutional',
            'etf', 'approval', 'regulation', 'investment', 'acquisition', 'expansion',
            'breakthrough', 'innovation', 'milestone', 'record', 'surpass', 'achieve'
        }
        
        self.bearish_keywords = {
            'hack', 'exploit', 'scam', 'fraud', 'ban', 'restriction', 'lawsuit',
            'investigation', 'delay', 'postpone', 'cancel', 'failure', 'breach',
            'vulnerability', 'crash', 'outage', 'suspend', 'fine', 'penalty'
        }
        
        self.high_impact_keywords = {
            'federal reserve', 'sec', 'regulation', 'ban', 'etf', 'institutional',
            'major', 'billion', 'fork', 'halving', 'upgrade', 'hack', 'bankruptcy'
        }
    
    def analyze_news_item(self, news_item: Dict) -> Dict[str, any]:
        """
        Analyze a single news item
        
        Args:
            news_item: Dictionary with 'title', 'content', 'source', 'published_at'
            
        Returns:
            News analysis results
        """
        if not self.enabled:
            return {'impact': 'neutral', 'sentiment': 'neutral', 'score': 0.5}
        
        title = news_item.get('title', '').lower()
        content = news_item.get('content', '').lower()
        full_text = f"{title} {content}"
        
        # Extract keywords
        words = set(re.findall(r'\b\w+\b', full_text))
        
        # Count bullish and bearish keywords
        bullish_count = len(words & self.bullish_keywords)
        bearish_count = len(words & self.bearish_keywords)
        high_impact_count = len(words & self.high_impact_keywords)
        
        # Calculate sentiment score
        total_keywords = bullish_count + bearish_count
        if total_keywords > 0:
            sentiment_score = bullish_count / total_keywords
        else:
            sentiment_score = 0.5  # Neutral
        
        # Determine sentiment
        if sentiment_score > 0.6:
            sentiment = 'bullish'
        elif sentiment_score < 0.4:
            sentiment = 'bearish'
        else:
            sentiment = 'neutral'
        
        # Determine impact level
        if high_impact_count >= 3 or total_keywords >= 5:
            impact = 'high'
        elif high_impact_count >= 1 or total_keywords >= 2:
            impact = 'medium'
        else:
            impact = 'low'
        
        # Calculate freshness (how recent is the news)
        published_at = news_item.get('published_at')
        freshness = self._calculate_freshness(published_at)
        
        return {
            'sentiment': sentiment,
            'sentiment_score': sentiment_score,
            'impact': impact,
            'freshness': freshness,
            'bullish_indicators': bullish_count,
            'bearish_indicators': bearish_count,
            'high_impact_indicators': high_impact_count,
            'source': news_item.get('source', 'unknown')
        }
    
    def _calculate_freshness(self, published_at) -> float:
        """Calculate news freshness score (0-1, 1 being most recent)"""
        if not published_at:
            return 0.5
        
        try:
            if isinstance(published_at, str):
                published_at = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            
            now = datetime.now(published_at.tzinfo)
            age = (now - published_at).total_seconds() / 3600  # Age in hours
            
            # Fresher news gets higher score
            if age < 1:
                return 1.0
            elif age < 6:
                return 0.8
            elif age < 24:
                return 0.6
            elif age < 72:
                return 0.4
            else:
                return 0.2
        except:
            return 0.5
    
    def analyze_news_batch(self, news_items: List[Dict]) -> Dict[str, any]:
        """
        Analyze multiple news items
        
        Args:
            news_items: List of news item dictionaries
            
        Returns:
            Aggregated news analysis
        """
        if not news_items:
            return {
                'signal': 'NEUTRAL',
                'overall_sentiment': 'neutral',
                'confidence': 0.0,
                'impact_level': 'low'
            }
        
        analyses = [self.analyze_news_item(item) for item in news_items]
        
        # Weight by freshness and impact
        weighted_scores = []
        weights = []
        
        for analysis in analyses:
            impact_weight = {'high': 3.0, 'medium': 2.0, 'low': 1.0}.get(analysis['impact'], 1.0)
            freshness_weight = analysis['freshness']
            
            weight = impact_weight * freshness_weight
            weights.append(weight)
            weighted_scores.append(analysis['sentiment_score'] * weight)
        
        # Calculate weighted average
        if sum(weights) > 0:
            overall_score = sum(weighted_scores) / sum(weights)
        else:
            overall_score = 0.5
        
        # Determine overall sentiment
        if overall_score > 0.6:
            overall_sentiment = 'bullish'
        elif overall_score < 0.4:
            overall_sentiment = 'bearish'
        else:
            overall_sentiment = 'neutral'
        
        # Determine impact level
        high_impact_count = sum(1 for a in analyses if a['impact'] == 'high')
        if high_impact_count >= 2:
            impact_level = 'high'
        elif high_impact_count >= 1 or len([a for a in analyses if a['impact'] == 'medium']) >= 3:
            impact_level = 'medium'
        else:
            impact_level = 'low'
        
        # Generate trading signal
        if overall_sentiment == 'bullish' and impact_level in ['high', 'medium']:
            signal = 'BUY'
            confidence = min(overall_score, 0.8)
        elif overall_sentiment == 'bearish' and impact_level in ['high', 'medium']:
            signal = 'SELL'
            confidence = min(1 - overall_score, 0.8)
        else:
            signal = 'HOLD'
            confidence = 0.5
        
        # Count by sentiment
        sentiment_counts = defaultdict(int)
        for analysis in analyses:
            sentiment_counts[analysis['sentiment']] += 1
        
        return {
            'signal': signal,
            'overall_sentiment': overall_sentiment,
            'sentiment_score': overall_score,
            'confidence': confidence,
            'impact_level': impact_level,
            'total_news': len(news_items),
            'sentiment_distribution': dict(sentiment_counts),
            'high_impact_news': high_impact_count
        }
    
    def get_trending_topics(self, news_items: List[Dict]) -> List[Dict[str, any]]:
        """
        Extract trending topics from news
        
        Args:
            news_items: List of news items
            
        Returns:
            List of trending topics with sentiment
        """
        topic_sentiments = defaultdict(list)
        topic_counts = defaultdict(int)
        
        # Common crypto topics to track
        topics = {
            'bitcoin': ['bitcoin', 'btc'],
            'ethereum': ['ethereum', 'eth'],
            'regulation': ['regulation', 'sec', 'regulatory'],
            'defi': ['defi', 'decentralized finance'],
            'nft': ['nft', 'non-fungible'],
            'mining': ['mining', 'miner'],
            'staking': ['staking', 'stake'],
            'exchange': ['exchange', 'trading platform']
        }
        
        for item in news_items:
            text = f"{item.get('title', '')} {item.get('content', '')}".lower()
            analysis = self.analyze_news_item(item)
            
            for topic, keywords in topics.items():
                if any(keyword in text for keyword in keywords):
                    topic_sentiments[topic].append(analysis['sentiment_score'])
                    topic_counts[topic] += 1
        
        # Calculate average sentiment per topic
        trending = []
        for topic, scores in topic_sentiments.items():
            if scores:
                avg_score = sum(scores) / len(scores)
                trending.append({
                    'topic': topic,
                    'mentions': topic_counts[topic],
                    'sentiment_score': avg_score,
                    'sentiment': 'bullish' if avg_score > 0.6 else 'bearish' if avg_score < 0.4 else 'neutral'
                })
        
        # Sort by number of mentions
        trending.sort(key=lambda x: x['mentions'], reverse=True)
        
        return trending
    
    def detect_market_events(self, news_items: List[Dict]) -> List[Dict[str, any]]:
        """
        Detect significant market events from news
        
        Args:
            news_items: List of news items
            
        Returns:
            List of detected market events
        """
        events = []
        
        event_patterns = {
            'regulatory': ['sec', 'regulation', 'ban', 'approval', 'regulatory'],
            'partnership': ['partnership', 'collaborate', 'integration', 'partnership'],
            'security': ['hack', 'exploit', 'breach', 'vulnerability', 'security'],
            'adoption': ['adoption', 'accept', 'payment', 'merchant', 'institutional'],
            'technology': ['upgrade', 'fork', 'launch', 'release', 'update'],
            'financial': ['investment', 'funding', 'acquisition', 'ipo', 'listing']
        }
        
        for item in news_items:
            text = f"{item.get('title', '')} {item.get('content', '')}".lower()
            analysis = self.analyze_news_item(item)
            
            if analysis['impact'] in ['high', 'medium']:
                for event_type, keywords in event_patterns.items():
                    if any(keyword in text for keyword in keywords):
                        events.append({
                            'type': event_type,
                            'title': item.get('title', ''),
                            'sentiment': analysis['sentiment'],
                            'impact': analysis['impact'],
                            'source': item.get('source', ''),
                            'published_at': item.get('published_at', '')
                        })
                        break  # Only categorize as one event type
        
        return events
