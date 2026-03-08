#!/usr/bin/env python3
"""
⏰ Polymarket Auto-Scheduler - FREE Version
Automatically runs scraper every 5 minutes
Author: Agent Claw 🦾
Date: 2026-03-08
"""

import schedule
import time
import subprocess
import sys
from datetime import datetime
from pathlib import Path

class PolymarketScheduler:
    """Automate Polymarket scraping"""
    
    def __init__(self, interval_minutes=5):
        self.interval = interval_minutes
        self.log_file = Path("data/logs/scheduler.log")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log(self, message):
        """Log message to file and console"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        
        print(log_entry)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
    
    def run_scraper(self):
        """Run scraper.py"""
        self.log("🚀 Starting scraper...")
        
        try:
            result = subprocess.run(
                [sys.executable, 'tools/scraper.py'],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                self.log("✅ Scraper completed successfully")
            else:
                self.log(f"❌ Scraper failed: {result.stderr}")
            
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            self.log("❌ Scraper timed out (5 minutes)")
            return False
        except Exception as e:
            self.log(f"❌ Error running scraper: {str(e)}")
            return False
    
    def run_alerter(self):
        """Run alerter.py to check for alerts"""
        self.log("🚨 Checking alerts...")
        
        try:
            result = subprocess.run(
                [sys.executable, 'tools/alerter.py'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                self.log("✅ Alerts checked")
            else:
                self.log(f"❌ Alert check failed: {result.stderr}")
            
            return result.returncode == 0
            
        except Exception as e:
            self.log(f"❌ Error checking alerts: {str(e)}")
            return False
    
    def job(self):
        """Scheduled job"""
        self.log("=" * 60)
        self.log("⏰ Scheduled Job Starting...")
        
        # Run scraper
        scraper_success = self.run_scraper()
        
        # Run alerter if scraper succeeded
        if scraper_success:
            self.run_alerter()
        
        self.log("⏰ Job Complete")
        self.log("=" * 60)
    
    def start(self):
        """Start the scheduler"""
        self.log("🎯 Polymarket Scheduler - Starting...")
        self.log(f"⏱️  Interval: Every {self.interval} minutes")
        self.log("📝 Log file: " + str(self.log_file.absolute()))
        
        # Schedule job
        schedule.every(self.interval).minutes.do(self.job)
        
        self.log("✅ Scheduler started! Press Ctrl+C to stop")
        
        # Run initial job
        self.log("🔄 Running initial job...")
        self.job()
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(1)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Polymarket Auto-Scheduler')
    parser.add_argument('--interval', type=int, default=5, 
                       help='Scrape interval in minutes (default: 5)')
    
    args = parser.parse_args()
    
    scheduler = PolymarketScheduler(interval_minutes=args.interval)
    
    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("\n\n⏹️  Scheduler stopped by user")
    except Exception as e:
        print(f"\n\n❌ Scheduler crashed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
