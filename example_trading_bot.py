"""
Example usage of the AI Trading Bot
"""

import json
from trading_bot_ai import TradingBot, Config


def main():
    """Main example function"""
    print("=" * 60)
    print("AI-Powered Cryptocurrency Trading Bot")
    print("=" * 60)
    print()
    
    # Initialize the trading bot
    print("Initializing trading bot...")
    bot = TradingBot()
    print("✓ Bot initialized successfully\n")
    
    # Display configuration
    print("Configuration:")
    print(f"  - Symbols: {bot.config.get('trading.symbols')}")
    print(f"  - Initial Capital: ${bot.config.get('trading.initial_capital'):,.2f}")
    print(f"  - Max Position Size: {bot.config.get('trading.max_position_size')*100}%")
    print(f"  - Risk per Trade: {bot.config.get('risk_management.risk_per_trade')*100}%")
    print()
    
    # Run analysis cycle
    print("Running analysis cycle...")
    print("-" * 60)
    
    results = bot.run_analysis_cycle()
    
    # Display results for each symbol
    for symbol, result in results.items():
        if 'error' in result:
            print(f"\n❌ {symbol}: Error - {result['error']}")
            continue
        
        analysis = result['analysis']
        decision = result['decision']
        
        print(f"\n📊 Analysis Results for {symbol}")
        print(f"   Current Price: ${analysis['current_price']:,.2f}")
        print()
        
        # Technical Analysis
        tech = analysis['technical']
        print(f"   Technical Analysis:")
        print(f"   └─ Signal: {tech['signal']} (Confidence: {tech['confidence']:.2%})")
        print(f"      RSI: {tech['indicators']['RSI']:.2f}")
        print(f"      MACD: {tech['indicators']['MACD']:.2f}")
        print()
        
        # Fundamental Analysis
        fund = analysis['fundamental']
        print(f"   Fundamental Analysis:")
        print(f"   └─ Signal: {fund['signal']} (Score: {fund['score']:.2%})")
        print(f"      Risk Level: {fund['risk']['risk_level']}")
        print()
        
        # Sentiment Analysis
        sent = analysis['sentiment']
        print(f"   Sentiment Analysis:")
        print(f"   └─ Signal: {sent['signal']} (Score: {sent['score']:.2%})")
        print(f"      Fear & Greed Index: {sent['fear_greed_index']['index']}/100")
        print(f"      Category: {sent['fear_greed_index']['category']}")
        print()
        
        # News Analysis
        news = analysis['news']
        print(f"   News Analysis:")
        print(f"   └─ Signal: {news['signal']}")
        print(f"      Overall Sentiment: {news['sentiment']}")
        print(f"      Impact Level: {news['impact']}")
        if news['events']:
            print(f"      Recent Events: {len(news['events'])} detected")
        print()
        
        # Final Decision
        print(f"   🎯 FINAL DECISION: {decision['decision']}")
        print(f"   Confidence: {decision['confidence']:.2%}")
        print(f"   Weighted Score: {decision['weighted_score']:.2%}")
        print()
        
        # Risk Assessment
        risk = decision['risk_assessment']
        print(f"   Risk Assessment:")
        print(f"   └─ Risk Level: {risk['risk_level']}")
        print(f"      Risk Score: {risk['risk_score']:.2%}")
        print(f"      Recommendation: {risk['recommendation']}")
        if risk['risk_factors']:
            print(f"      Risk Factors:")
            for factor in risk['risk_factors']:
                print(f"        • {factor}")
        print()
        
        # Execute trade (simulation)
        if decision['decision'] != 'HOLD':
            print(f"   Executing {decision['decision']} order...")
            trade_result = bot.execute_trade(decision)
            
            if trade_result['status'] == 'executed':
                position = trade_result['position']
                print(f"   ✓ Trade executed successfully!")
                print(f"     Position Size: {position['position_size']:.4f} {symbol.split('/')[0]}")
                print(f"     Position Value: ${position['position_value']:,.2f}")
                print(f"     Stop Loss: ${position['stop_loss']:,.2f}")
                print(f"     Take Profit Levels: ", end="")
                print(f"${position['take_profit_levels'][0]:,.2f}, ", end="")
                print(f"${position['take_profit_levels'][1]:,.2f}, ", end="")
                print(f"${position['take_profit_levels'][2]:,.2f}")
            else:
                print(f"   ℹ {trade_result.get('message', 'Trade not executed')}")
        
        print("-" * 60)
    
    # Display bot status
    print("\n📈 Bot Status:")
    status = bot.get_status()
    print(f"   Current Capital: ${status['capital']:,.2f}")
    print(f"   Open Positions: {status['open_positions']}")
    
    if status['open_positions'] > 0:
        print("\n   Active Positions:")
        for position in status['positions']:
            print(f"   • {position['symbol']}: {position['type'].upper()}")
            print(f"     Entry: ${position['entry_price']:,.2f}")
            print(f"     Size: {position['position_size']:.4f}")
    
    # Display performance report
    print("\n📊 Performance Report:")
    report = bot.get_performance_report()
    print(f"   Total P&L: ${report['total_pnl']:,.2f} ({report['pnl_percentage']:.2f}%)")
    print(f"   Total Trades: {report['total_trades']}")
    print(f"   Win Rate: {report['win_rate']:.1f}%")
    print(f"   Winning Trades: {report['winning_trades']}")
    print(f"   Losing Trades: {report['losing_trades']}")
    
    print("\n" + "=" * 60)
    print("Analysis cycle completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
