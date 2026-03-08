#!/usr/bin/env python3
"""
🕷️ Polymarket Advanced Scraper - FREE Version
Scrapes multiple markets with better error handling
Author: Agent Claw 🦾
Date: 2026-03-08
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime
import time
from pathlib import Path
import random

class AdvancedPolymarketScraper:
    """Advanced Polymarket scraper with better error handling"""
    
    def __init__(self):
        self.base_url = "https://polymarket.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        })
        
        # Create directories
        self.data_dir = Path("data/markets")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Market categories
        self.categories = {
            'politics': [
                'will-the-iranian-regime-fall-by-june-30',
                # Add more politics markets
            ],
            'crypto': [
                # Add crypto markets
            ],
            'sports': [
                # Add sports markets
            ]
        }
    
    def fetch_market_advanced(self, market_slug, category='other'):
        """
        Fetch market with advanced error handling
        
        Args:
            market_slug: Market slug (e.g., 'will-the-iranian-regime-fall-by-june-30')
            category: Market category
            
        Returns:
            Dictionary with market data or None
        """
        url = f"{self.base_url}/event/{market_slug}"
        
        try:
            print(f"🔍 [{category.upper()}] Fetching: {market_slug}")
            
            # Add random delay to avoid rate limiting
            time.sleep(random.uniform(1, 3))
            
            response = self.session.get(url, timeout=15)
            
            # Check for common errors
            if response.status_code == 404:
                print(f"⚠️  404 - Market not found: {market_slug}")
                return None
            elif response.status_code == 429:
                print(f"⚠️  429 - Rate limited, waiting 30s...")
                time.sleep(30)
                return None
            elif response.status_code != 200:
                print(f"❌ HTTP {response.status_code} for {market_slug}")
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract data
            data = {
                'slug': market_slug,
                'category': category,
                'title': self._extract_title(soup),
                'yes_price': self._extract_price(soup, 'Yes'),
                'no_price': self._extract_price(soup, 'No'),
                'volume_24h': self._extract_volume(soup),
                'liquidity': self._extract_liquidity(soup),
                'timestamp': datetime.now().isoformat(),
                'status': 'success'
            }
            
            print(f"✅ Success: {data['title'][:50]}...")
            return data
            
        except requests.exceptions.Timeout:
            print(f"❌ Timeout: {market_slug}")
            return {'slug': market_slug, 'status': 'timeout', 'timestamp': datetime.now().isoformat()}
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {str(e)}")
            return {'slug': market_slug, 'status': 'error', 'error': str(e), 'timestamp': datetime.now().isoformat()}
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return {'slug': market_slug, 'status': 'error', 'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    def _extract_title(self, soup):
        """Extract market title"""
        try:
            title = soup.find('h1') or soup.find('title')
            return title.get_text(strip=True) if title else 'N/A'
        except:
            return 'N/A'
    
    def _extract_price(self, soup, outcome):
        """Extract price for Yes/No"""
        try:
            # Placeholder - adjust based on actual HTML
            return 0.50
        except:
            return 0.00
    
    def _extract_volume(self, soup):
        """Extract 24h volume"""
        try:
            return 0
        except:
            return 0
    
    def _extract_liquidity(self, soup):
        """Extract liquidity"""
        try:
            return 0
        except:
            return 0
    
    def scrape_all_categories(self):
        """Scrape all markets from all categories"""
        print("🚀 Advanced Scraper - Starting...")
        print("=" * 60)
        
        all_results = []
        
        for category, markets in self.categories.items():
            print(f"\n📂 Category: {category.upper()} ({len(markets)} markets)")
            
            for market in markets:
                data = self.fetch_market_advanced(market, category)
                if data:
                    all_results.append(data)
        
        # Save results
        if all_results:
            self._save_results(all_results)
        
        # Summary
        success = len([r for r in all_results if r.get('status') == 'success'])
        total = len(all_results)
        
        print("\n" + "=" * 60)
        print("📊 Scraping Summary:")
        print(f"  Total Markets: {total}")
        print(f"  Successful: {success}")
        print(f"  Failed: {total - success}")
        print(f"  Success Rate: {(success/total)*100:.1f}%")
        print("=" * 60)
        
        return all_results
    
    def _save_results(self, results):
        """Save results to CSV"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"data/markets/advanced_scrape_{timestamp}.csv"
        
        df = pd.DataFrame(results)
        df.to_csv(filename, index=False, encoding='utf-8')
        
        print(f"💾 Saved {len(results)} records to {filename}")
        
        # Also save to JSON
        json_file = f"data/markets/advanced_scrape_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved JSON to {json_file}")


def main():
    """Main entry point"""
    scraper = AdvancedPolymarketScraper()
    scraper.scrape_all_categories()


if __name__ == "__main__":
    main()