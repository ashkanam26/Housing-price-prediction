"""
Fundamental Analysis Module for Cryptocurrency
"""

import pandas as pd
import numpy as np
from typing import Dict, List


class FundamentalAnalyzer:
    """Fundamental analysis for cryptocurrency assets"""
    
    def __init__(self, config: Dict):
        """
        Initialize fundamental analyzer
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.enabled = config.get('fundamental_analysis', {}).get('enabled', True)
    
    def analyze_fundamentals(self, asset_data: Dict) -> Dict[str, any]:
        """
        Analyze fundamental metrics
        
        Args:
            asset_data: Dictionary containing fundamental data
            
        Returns:
            Analysis results
        """
        if not self.enabled:
            return {'score': 0.5, 'signal': 'NEUTRAL', 'factors': {}}
        
        scores = []
        factors = {}
        
        # Market Cap Analysis
        market_cap = asset_data.get('market_cap', 0)
        if market_cap > 10_000_000_000:  # > 10B
            scores.append(1.0)
            factors['market_cap'] = 'Strong - High market cap'
        elif market_cap > 1_000_000_000:  # > 1B
            scores.append(0.7)
            factors['market_cap'] = 'Good - Medium market cap'
        else:
            scores.append(0.4)
            factors['market_cap'] = 'Risky - Low market cap'
        
        # Volume Analysis
        volume_24h = asset_data.get('volume_24h', 0)
        avg_volume = asset_data.get('avg_volume', 1)
        volume_ratio = volume_24h / max(avg_volume, 1)
        
        if volume_ratio > 1.5:
            scores.append(0.8)
            factors['volume'] = 'High trading activity'
        elif volume_ratio > 0.8:
            scores.append(0.6)
            factors['volume'] = 'Normal trading activity'
        else:
            scores.append(0.3)
            factors['volume'] = 'Low trading activity'
        
        # Liquidity Analysis
        liquidity_score = asset_data.get('liquidity_score', 0.5)
        scores.append(liquidity_score)
        factors['liquidity'] = f'Liquidity score: {liquidity_score:.2f}'
        
        # Price Change Analysis
        price_change_24h = asset_data.get('price_change_24h', 0)
        price_change_7d = asset_data.get('price_change_7d', 0)
        
        if price_change_24h > 5 and price_change_7d > 10:
            scores.append(0.8)
            factors['price_trend'] = 'Strong upward trend'
        elif price_change_24h > 0 and price_change_7d > 0:
            scores.append(0.6)
            factors['price_trend'] = 'Positive trend'
        elif price_change_24h < -5 and price_change_7d < -10:
            scores.append(0.2)
            factors['price_trend'] = 'Strong downward trend'
        else:
            scores.append(0.5)
            factors['price_trend'] = 'Neutral trend'
        
        # Market Dominance
        market_dominance = asset_data.get('market_dominance', 0)
        if market_dominance > 40:  # Like Bitcoin
            scores.append(1.0)
            factors['dominance'] = 'High market dominance'
        elif market_dominance > 5:
            scores.append(0.7)
            factors['dominance'] = 'Moderate market dominance'
        else:
            scores.append(0.5)
            factors['dominance'] = 'Low market dominance'
        
        # Calculate overall score
        overall_score = np.mean(scores)
        
        # Generate signal
        if overall_score > 0.7:
            signal = 'BULLISH'
        elif overall_score > 0.5:
            signal = 'NEUTRAL'
        else:
            signal = 'BEARISH'
        
        return {
            'score': overall_score,
            'signal': signal,
            'factors': factors,
            'confidence': abs(overall_score - 0.5) * 2  # 0 to 1 scale
        }
    
    def compare_assets(self, assets_data: List[Dict]) -> List[Dict]:
        """
        Compare multiple assets based on fundamentals
        
        Args:
            assets_data: List of asset data dictionaries
            
        Returns:
            Ranked list of assets
        """
        results = []
        
        for asset in assets_data:
            analysis = self.analyze_fundamentals(asset)
            results.append({
                'symbol': asset.get('symbol', 'Unknown'),
                'score': analysis['score'],
                'signal': analysis['signal'],
                'factors': analysis['factors']
            })
        
        # Sort by score (descending)
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results
    
    def get_risk_assessment(self, asset_data: Dict) -> Dict[str, any]:
        """
        Assess risk level based on fundamental factors
        
        Args:
            asset_data: Asset fundamental data
            
        Returns:
            Risk assessment dictionary
        """
        risk_factors = []
        risk_score = 0.5  # Neutral starting point
        
        # Volatility check
        volatility = asset_data.get('volatility_30d', 0)
        if volatility > 0.5:
            risk_score += 0.2
            risk_factors.append('High volatility')
        elif volatility > 0.3:
            risk_score += 0.1
            risk_factors.append('Moderate volatility')
        
        # Market cap risk
        market_cap = asset_data.get('market_cap', 0)
        if market_cap < 100_000_000:  # < 100M
            risk_score += 0.2
            risk_factors.append('Small market cap')
        
        # Liquidity risk
        liquidity_score = asset_data.get('liquidity_score', 1.0)
        if liquidity_score < 0.3:
            risk_score += 0.15
            risk_factors.append('Low liquidity')
        
        # Price decline risk
        price_change_30d = asset_data.get('price_change_30d', 0)
        if price_change_30d < -30:
            risk_score += 0.15
            risk_factors.append('Significant recent decline')
        
        # Cap risk score at 1.0
        risk_score = min(risk_score, 1.0)
        
        # Determine risk level
        if risk_score > 0.7:
            risk_level = 'HIGH'
        elif risk_score > 0.5:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'risk_factors': risk_factors,
            'recommendation': self._get_risk_recommendation(risk_level)
        }
    
    def _get_risk_recommendation(self, risk_level: str) -> str:
        """Get recommendation based on risk level"""
        recommendations = {
            'HIGH': 'Exercise caution. Consider smaller position sizes or avoid.',
            'MEDIUM': 'Moderate risk. Use appropriate position sizing and stop losses.',
            'LOW': 'Lower risk. Suitable for standard position sizing.'
        }
        return recommendations.get(risk_level, 'Unknown risk level')
