#!/usr/bin/env python3
"""
💰 Polymarket Arbitrage Detector - FREE Version
Finds arbitrage opportunities across markets
Author: Agent Claw 🦾
Date: 2026-03-08
"""

import pandas as pd
import json
from datetime import datetime
from pathlib import Path
import glob

class ArbitrageDetector:
    """Detect arbitrage opportunities"""
    
    def __init__(self):
        self.data_dir = Path("data/markets")
    
    def load_latest_data(self):
        """Load latest scraping data"""
        csv_files = glob.glob(str(self.data_dir / "scrape_*.csv"))
        
        if not csv_files:
            return None
        
        latest = max(csv_files)
        return pd.read_csv(latest)
    
    def detect_arbitrage(self, df):
        """
        Detect arbitrage opportunities
        
        Arbitrage exists when:
        Yes Price + No Price < 1.00 (buy both, guaranteed profit)
        """
        print("💰 Arbitrage Detector - Starting...")
        print("=" * 60)
        
        opportunities = []
        
        if df is None or len(df) == 0:
            print("⚠️  No data available")
            return opportunities
        
        for _, row in df.iterrows():
            yes_price = row.get('yes_price', 0.5)
            no_price = row.get('no_price', 0.5)
            
            # Check for arbitrage
            total_price = yes_price + no_price
            
            if total_price < 0.95:  # 5%+ profit margin
                profit = 1.00 - total_price
                roi = (profit / total_price) * 100
                
                opportunity = {
                    'market': row.get('title', 'Unknown'),
                    'yes_price': yes_price,
                    'no_price': no_price,
                    'total_price': total_price,
                    'profit_margin': profit,
                    'roi_percent': roi,
                    'strategy': 'BUY_BOTH',
                    'timestamp': datetime.now().isoformat()
                }
                
                opportunities.append(opportunity)
                
                print(f"\n💎 ARBITRAGE FOUND!")
                print(f"  Market: {opportunity['market']}")
                print(f"  Yes: ${yes_price:.3f}")
                print(f"  No: ${no_price:.3f}")
                print(f"  Total: ${total_price:.3f}")
                print(f"  Profit: ${profit:.3f} ({roi:.1f}% ROI)")
        
        if not opportunities:
            print("\n⚠️  No arbitrage opportunities found")
            print("💡 This is normal - efficient markets rarely have arbitrage")
        else:
            print(f"\n✅ Found {len(opportunities)} arbitrage opportunities!")
        
        # Save
        if opportunities:
            self._save_opportunities(opportunities)
        
        return opportunities
    
    def _save_opportunities(self, opportunities):
        """Save opportunities to JSON"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"data/models/arbitrage_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(opportunities, f, indent=2)
        
        print(f"💾 Saved to: {filename}")


def main():
    """Main entry point"""
    detector = ArbitrageDetector()
    df = detector.load_latest_data()
    detector.detect_arbitrage(df)


if __name__ == "__main__":
    main()