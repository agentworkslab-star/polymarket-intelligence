#!/usr/bin/env python3
"""
📊 Polymarket Performance Analytics
Track win rate, ROI, and performance
Author: Agent Claw 🦾
Date: 2026-03-08
"""

import pandas as pd
import json
from datetime import datetime
from pathlib import Path

class PerformanceAnalytics:
    """Track trading performance"""
    
    def __init__(self):
        self.data_file = Path("data/performance/trades.json")
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log_trade(self, market, action, probability, stake, result=None):
        """Log a trade"""
        trade = {
            'market': market,
            'action': action,  # BUY/SELL
            'probability': probability,
            'stake': stake,
            'result': result,  # WIN/LOSS/PENDING
            'timestamp': datetime.now().isoformat()
        }
        
        trades = self.load_trades()
        trades.append(trade)
        self.save_trades(trades)
        
        print(f"✅ Trade logged: {market} ({action})")
    
    def load_trades(self):
        """Load all trades"""
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_trades(self, trades):
        """Save trades"""
        with open(self.data_file, 'w') as f:
            json.dump(trades, f, indent=2)
    
    def calculate_stats(self):
        """Calculate performance statistics"""
        trades = self.load_trades()
        
        if not trades:
            print("⚠️  No trades logged")
            return
        
        df = pd.DataFrame(trades)
        
        total_trades = len(df)
        completed = df[df['result'].isin(['WIN', 'LOSS'])]
        
        wins = len(completed[completed['result'] == 'WIN'])
        losses = len(completed[completed['result'] == 'LOSS'])
        win_rate = (wins / len(completed) * 100) if len(completed) > 0 else 0
        
        print("📊 Performance Analytics")
        print("=" * 60)
        print(f"Total Trades: {total_trades}")
        print(f"Completed: {len(completed)}")
        print(f"Wins: {wins}")
        print(f"Losses: {losses}")
        print(f"Win Rate: {win_rate:.1f}%")
        print("=" * 60)


def main():
    """Test analytics"""
    analytics = PerformanceAnalytics()
    analytics.calculate_stats()


if __name__ == "__main__":
    main()