#!/usr/bin/env python3
"""
Quick Start Script for Cryptocurrency Trading Bot
Run this to quickly test the bot
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crypto_bot.bot import CryptoTradingBot


def main():
    print("="*70)
    print(" 🤖 CRYPTOCURRENCY TRADING BOT - QUICK START")
    print("="*70)
    print()
    print("This script will:")
    print("  1. Initialize the trading bot")
    print("  2. Train ML/DL models on historical data")
    print("  3. Run the bot for 10 iterations")
    print("  4. Display performance summary")
    print()
    print("⚠️  WARNING: This uses simulated data for demonstration")
    print()
    
    # Configuration
    symbol = input("Enter trading pair (default: BTC/USDT): ").strip() or "BTC/USDT"
    
    try:
        capital_input = input("Enter initial capital (default: 10000): ").strip()
        initial_capital = float(capital_input) if capital_input else 10000
    except ValueError:
        initial_capital = 10000
        print("Invalid input, using default: 10000")
    
    try:
        iterations_input = input("Enter number of iterations (default: 10): ").strip()
        iterations = int(iterations_input) if iterations_input else 10
    except ValueError:
        iterations = 10
        print("Invalid input, using default: 10")
    
    print()
    print("-"*70)
    print(f"Configuration:")
    print(f"  Symbol: {symbol}")
    print(f"  Initial Capital: ${initial_capital:,.2f}")
    print(f"  Iterations: {iterations}")
    print("-"*70)
    print()
    
    input("Press Enter to start...")
    print()
    
    try:
        # Initialize bot
        print("Step 1: Initializing trading bot...")
        bot = CryptoTradingBot(
            symbol=symbol,
            initial_capital=initial_capital,
            timeframe='1h',
            lookback=60
        )
        print("✅ Bot initialized successfully!\n")
        
        # Train models
        print("Step 2: Training ML/DL models...")
        print("(This may take a moment...)")
        bot.train_models(historical_periods=500)
        print("✅ Models trained successfully!\n")
        
        # Run bot
        print("Step 3: Starting trading bot...")
        print("-"*70)
        final_performance = bot.run(iterations=iterations, interval=5)
        
        # Summary
        print()
        print("="*70)
        print(" 📊 FINAL PERFORMANCE SUMMARY")
        print("="*70)
        print(f"Initial Capital:    ${bot.initial_capital:>12,.2f}")
        print(f"Final Capital:      ${final_performance['current_capital']:>12,.2f}")
        print(f"Total Return:       ${final_performance['total_return']:>12,.2f}")
        print(f"Return Percentage:  {final_performance['total_return_pct']:>12.2f}%")
        print("-"*70)
        print(f"Total Trades:       {final_performance['total_trades']:>12}")
        print(f"Winning Trades:     {final_performance['winning_trades']:>12}")
        print(f"Losing Trades:      {final_performance['losing_trades']:>12}")
        print(f"Win Rate:           {final_performance['win_rate']:>12.2f}%")
        print("="*70)
        print()
        
        if final_performance['total_return'] > 0:
            print("🎉 Profitable session!")
        elif final_performance['total_return'] < 0:
            print("📉 Loss in this session")
        else:
            print("➡️  Break-even session")
        
        print()
        print("💡 Next Steps:")
        print("  - Run 'python crypto_bot/web/app.py' for web interface")
        print("  - Open 'crypto_bot_demo.ipynb' for detailed examples")
        print("  - Read 'CRYPTO_BOT_README.md' for full documentation")
        print()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        if bot:
            bot.stop()
        print("Bot stopped safely")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
