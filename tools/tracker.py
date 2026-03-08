#!/usr/bin/env python3
"""
📊 Polymarket Data Tracker - FREE Version
Tracks market data in Google Sheets
Author: Agent Claw 🦾
Date: 2026-03-08
"""

import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from pathlib import Path
import json

class MarketTracker:
    """Track Polymarket data in Google Sheets"""
    
    def __init__(self, sheet_name="Polymarket - Market Tracker"):
        self.sheet_name = sheet_name
        self.gc = None
        self.sheet = None
        
        # Create data directories
        self.data_dir = Path("data/markets")
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def connect_google_sheets(self, credentials_file="config/credentials.json"):
        """
        Connect to Google Sheets API
        
        Args:
            credentials_file: Path to Google credentials JSON file
        """
        try:
            print("🔗 Connecting to Google Sheets...")
            
            # Define scopes
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Load credentials
            creds = Credentials.from_service_account_file(
                credentials_file,
                scopes=scopes
            )
            
            self.gc = gspread.authorize(creds)
            
            # Open or create spreadsheet
            try:
                self.sheet = self.gc.open(self.sheet_name).sheet1
                print(f"✅ Connected to: {self.sheet_name}")
            except gspread.exceptions.SpreadsheetNotFound:
                print(f"📝 Creating new spreadsheet: {self.sheet_name}")
                new_spreadsheet = self.gc.create(self.sheet_name)
                self.sheet = new_spreadsheet.sheet1
                
                # Setup headers
                self._setup_headers()
                print("✅ Spreadsheet created and headers setup")
            
            return True
            
        except FileNotFoundError:
            print(f"❌ Credentials file not found: {credentials_file}")
            print("\n📋 Setup Instructions:")
            print("1. Go to: https://console.cloud.google.com/")
            print("2. Create new project or select existing")
            print("3. Enable Google Sheets API & Google Drive API")
            print("4. Create credentials (Service Account)")
            print("5. Download JSON key file")
            print("6. Save as: config/credentials.json")
            print("7. Share Google Sheet with service account email")
            return False
        except Exception as e:
            print(f"❌ Error connecting: {str(e)}")
            return False
    
    def _setup_headers(self):
        """Setup column headers in Google Sheet"""
        headers = [
            'Market ID',
            'Market Name',
            'Category',
            'Question',
            'Outcome',
            'Probability (%)',
            'Price ($)',
            '24h Volume ($)',
            'Total Liquidity ($)',
            'Days to Resolution',
            'Risk Score (1-10)',
            'Decision',
            'Position Size (%)',
            'Entry Price',
            'Target Price',
            'Stop Loss',
            'Status',
            'Notes',
            'Last Updated'
        ]
        
        self.sheet.update('A1:S1', [headers])
        
        # Format header row
        self.sheet.format('A1:S1', {
            'backgroundColor': {'red': 0.2, 'green': 0.6, 'blue': 1.0},
            'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}}
        })
    
    def load_csv_data(self, csv_file):
        """
        Load data from CSV file
        
        Args:
            csv_file: Path to CSV file
            
        Returns:
            DataFrame with market data
        """
        try:
            print(f"📂 Loading data from: {csv_file}")
            df = pd.read_csv(csv_file)
            print(f"✅ Loaded {len(df)} records")
            return df
        except Exception as e:
            print(f"❌ Error loading CSV: {str(e)}")
            return None
    
    def append_to_sheet(self, df):
        """
        Append DataFrame rows to Google Sheet
        
        Args:
            df: pandas DataFrame with market data
        """
        if self.sheet is None:
            print("❌ Not connected to Google Sheets")
            return False
        
        try:
            print(f"📊 Appending {len(df)} records to sheet...")
            
            # Convert DataFrame to list of lists
            values = df.values.tolist()
            
            # Get next empty row
            next_row = len(self.sheet.get_all_values()) + 1
            
            if next_row == 1:
                # First row, add headers
                headers = df.columns.tolist()
                self.sheet.update('A1:S1', [headers])
                next_row = 2
            
            # Append data
            if values:
                cell_range = f'A{next_row}'
                self.sheet.update(cell_range, values)
                print(f"✅ Successfully appended {len(values)} records")
            
            return True
            
        except Exception as e:
            print(f"❌ Error appending to sheet: {str(e)}")
            return False
    
    def update_probability(self, market_id, new_probability):
        """
        Update probability for a specific market
        
        Args:
            market_id: Market identifier
            new_probability: New probability percentage
        """
        try:
            print(f"📈 Updating probability for {market_id}: {new_probability}%")
            
            # Find market in sheet
            all_data = self.sheet.get_all_values()
            
            for i, row in enumerate(all_data[1:], 2):  # Skip header
                if row[0] == market_id:  # Market ID column
                    # Update probability (column F = index 5)
                    self.sheet.update(f'F{i}', new_probability)
                    self.sheet.update(f'S{i}', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    print(f"✅ Updated row {i}")
                    return True
            
            print(f"⚠️ Market {market_id} not found")
            return False
            
        except Exception as e:
            print(f"❌ Error updating: {str(e)}")
            return False
    
    def get_market_history(self, market_id):
        """
        Get historical data for a market
        
        Args:
            market_id: Market identifier
            
        Returns:
            List of historical records
        """
        try:
            all_data = self.sheet.get_all_values()
            
            history = []
            for row in all_data[1:]:  # Skip header
                if row[0] == market_id:
                    history.append({
                        'probability': row[5],
                        'timestamp': row[18],
                        'status': row[16]
                    })
            
            return history
            
        except Exception as e:
            print(f"❌ Error getting history: {str(e)}")
            return []
    
    def calculate_trend(self, market_id):
        """
        Calculate probability trend for a market
        
        Args:
            market_id: Market identifier
            
        Returns:
            Dictionary with trend data
        """
        history = self.get_market_history(market_id)
        
        if len(history) < 2:
            return {'trend': 'insufficient_data', 'change': 0}
        
        # Get last 2 records
        old_prob = float(history[-2]['probability'])
        new_prob = float(history[-1]['probability'])
        change = new_prob - old_prob
        
        if change > 5:
            trend = 'rising_fast'
        elif change > 0:
            trend = 'rising'
        elif change < -5:
            trend = 'falling_fast'
        elif change < 0:
            trend = 'falling'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'change': change,
            'old_probability': old_prob,
            'new_probability': new_prob
        }


def main():
    """Example usage"""
    
    print("📊 Polymarket Tracker - Starting...")
    print("=" * 60)
    
    # Initialize tracker
    tracker = MarketTracker(sheet_name="Polymarket - Market Tracker")
    
    # Connect to Google Sheets
    if not tracker.connect_google_sheets():
        print("\n⚠️ Google Sheets connection failed.")
        print("Follow the setup instructions above to configure credentials.")
        return
    
    # Load recent CSV data
    import glob
    csv_files = glob.glob("data/markets/scrape_*.csv")
    
    if csv_files:
        latest_csv = max(csv_files)
        df = tracker.load_csv_data(latest_csv)
        
        if df is not None:
            tracker.append_to_sheet(df)
    
    # Example: Update probability
    # tracker.update_probability("iran-regime-fall", 35.0)
    
    # Example: Get trend
    # trend = tracker.calculate_trend("iran-regime-fall")
    # print(f"Trend: {trend}")
    
    print("\n" + "=" * 60)
    print("✅ Tracker setup complete!")
    print("📊 View your sheet: https://sheets.google.com/")
    print("=" * 60)


if __name__ == "__main__":
    main()