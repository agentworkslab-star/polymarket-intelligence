#!/usr/bin/env python3
"""
🤖 Polymarket ML Predictions - FREE Version
Basic machine learning for probability prediction
Author: Agent Claw 🦾
Date: 2026-03-08
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import glob
import json

class MarketPredictor:
    """Simple ML-based market predictor"""
    
    def __init__(self):
        self.data_dir = Path("data/markets")
        self.models_dir = Path("data/models")
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        # Simple prediction model (placeholder for actual ML)
        self.model = None
    
    def load_historical_data(self):
        """Load all historical scraping data"""
        csv_files = glob.glob(str(self.data_dir / "scrape_*.csv"))
        
        if not csv_files:
            print("⚠️  No historical data found. Run scraper first!")
            return None
        
        all_data = []
        for file in sorted(csv_files):
            try:
                df = pd.read_csv(file)
                all_data.append(df)
                print(f"📂 Loaded: {file}")
            except Exception as e:
                print(f"⚠️  Error loading {file}: {e}")
        
        if all_data:
            combined = pd.concat(all_data, ignore_index=True)
            print(f"✅ Total records: {len(combined)}")
            return combined
        
        return None
    
    def calculate_moving_average(self, df, window=3):
        """Calculate moving average for probabilities"""
        if 'yes_price' not in df.columns:
            return None
        
        df_sorted = df.sort_values('timestamp')
        df_sorted['ma_3'] = df_sorted['yes_price'].rolling(window=window).mean()
        df_sorted['ma_5'] = df_sorted['yes_price'].rolling(window=5).mean()
        
        return df_sorted
    
    def calculate_trend(self, df):
        """Calculate probability trend"""
        if len(df) < 2:
            return 'insufficient_data'
        
        recent = df.tail(2)['yes_price'].values
        change = recent[-1] - recent[0]
        
        if change > 0.1:
            return 'strong_rise'
        elif change > 0.05:
            return 'rise'
        elif change > 0:
            return 'slight_rise'
        elif change == 0:
            return 'stable'
        elif change > -0.05:
            return 'slight_fall'
        elif change > -0.1:
            return 'fall'
        else:
            return 'strong_fall'
    
    def predict_next_probability(self, df):
        """
        Simple prediction based on trend and moving average
        
        Note: This is a basic statistical model.
        For production, use proper ML libraries (scikit-learn, etc.)
        """
        if len(df) < 3:
            return None, "Insufficient data"
        
        # Calculate features
        current_prob = df['yes_price'].iloc[-1]
        ma_3 = df['yes_price'].tail(3).mean()
        ma_5 = df['yes_price'].tail(5).mean() if len(df) >= 5 else ma_3
        
        # Calculate trend
        trend = self.calculate_trend(df)
        
        # Simple prediction logic
        if trend in ['strong_rise', 'rise']:
            predicted = current_prob + 0.05
        elif trend in ['strong_fall', 'fall']:
            predicted = current_prob - 0.05
        else:
            predicted = current_prob
        
        # Clamp to valid range
        predicted = max(0.01, min(0.99, predicted))
        
        confidence = self._calculate_confidence(df, trend)
        
        return predicted, confidence
    
    def _calculate_confidence(self, df, trend):
        """Calculate prediction confidence (0-100%)"""
        if len(df) < 3:
            return 30
        
        # More data = higher confidence
        data_points = min(len(df), 10)
        base_confidence = 30 + (data_points * 5)
        
        # Stable trend = higher confidence
        if trend == 'stable':
            base_confidence += 10
        elif trend in ['strong_rise', 'strong_fall']:
            base_confidence -= 10  # Volatile = less confident
        
        return min(95, max(20, base_confidence))
    
    def generate_predictions(self):
        """Generate predictions for all markets"""
        print("🤖 ML Predictions - Starting...")
        print("=" * 60)
        
        # Load data
        df = self.load_historical_data()
        
        if df is None or len(df) == 0:
            print("❌ No data to analyze")
            return
        
        # Group by market slug if available
        if 'slug' in df.columns:
            markets = df['slug'].unique()
        else:
            markets = [df['title'].iloc[0] if 'title' in df.columns else 'market']
        
        predictions = []
        
        for market in markets:
            print(f"\n📊 Analyzing: {market}")
            
            # Get market data
            if 'slug' in df.columns:
                market_df = df[df['slug'] == market].sort_values('timestamp')
            else:
                market_df = df.sort_values('timestamp')
            
            if len(market_df) < 2:
                print(f"⚠️  Insufficient data for {market}")
                continue
            
            # Calculate metrics
            current_prob = market_df['yes_price'].iloc[-1]
            trend = self.calculate_trend(market_df)
            predicted, confidence = self.predict_next_probability(market_df)
            
            # Generate recommendation
            if predicted and predicted > current_prob + 0.05:
                recommendation = "BUY"
            elif predicted and predicted < current_prob - 0.05:
                recommendation = "SELL"
            else:
                recommendation = "HOLD"
            
            prediction = {
                'market': market,
                'current_probability': current_prob,
                'predicted_probability': predicted,
                'trend': trend,
                'confidence': confidence,
                'recommendation': recommendation,
                'timestamp': datetime.now().isoformat()
            }
            
            predictions.append(prediction)
            
            print(f"  Current: {current_prob*100:.1f}%")
            print(f"  Predicted: {predicted*100:.1f}% (±{100-confidence:.0f}%)")
            print(f"  Trend: {trend}")
            print(f"  Recommendation: {recommendation}")
        
        # Save predictions
        if predictions:
            self._save_predictions(predictions)
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 Prediction Summary:")
        print(f"  Markets Analyzed: {len(predictions)}")
        print(f"  BUY Recommendations: {len([p for p in predictions if p['recommendation'] == 'BUY'])}")
        print(f"  SELL Recommendations: {len([p for p in predictions if p['recommendation'] == 'SELL'])}")
        print(f"  HOLD Recommendations: {len([p for p in predictions if p['recommendation'] == 'HOLD'])}")
        print("=" * 60)
        
        return predictions
    
    def _save_predictions(self, predictions):
        """Save predictions to JSON"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"data/models/predictions_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(predictions, f, indent=2)
        
        print(f"💾 Predictions saved to: {filename}")
        
        # Also save to CSV
        df = pd.DataFrame(predictions)
        csv_file = f"data/models/predictions_{timestamp}.csv"
        df.to_csv(csv_file, index=False)
        print(f"💾 CSV saved to: {csv_file}")


def main():
    """Main entry point"""
    predictor = MarketPredictor()
    predictor.generate_predictions()


if __name__ == "__main__":
    main()