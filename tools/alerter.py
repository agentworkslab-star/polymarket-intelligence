#!/usr/bin/env python3
"""
🚨 Polymarket Alert System - FREE Version
Sends Telegram alerts on significant probability changes
Author: Agent Claw 🦾
Date: 2026-03-08
"""

import requests
import os
from datetime import datetime
from pathlib import Path
import json

class TelegramAlerter:
    """Send Polymarket alerts via Telegram"""
    
    def __init__(self, bot_token=None, chat_id=None, config_file="config/telegram_config.json"):
        self.config_file = Path(config_file)
        
        # Load or setup config
        if bot_token and chat_id:
            self.bot_token = bot_token
            self.chat_id = chat_id
            self._save_config()
        else:
            self._load_config()
        
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def _save_config(self):
        """Save Telegram config to file"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        
        config = {
            'bot_token': self.bot_token,
            'chat_id': self.chat_id,
            'created': datetime.now().isoformat()
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"💾 Config saved to: {self.config_file}")
    
    def _load_config(self):
        """Load Telegram config from file"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            self.bot_token = config.get('bot_token')
            self.chat_id = config.get('chat_id')
            
            if not self.bot_token or not self.chat_id:
                raise ValueError("Missing bot_token or chat_id")
            
            print(f"✅ Config loaded from: {self.config_file}")
            
        except FileNotFoundError:
            print(f"❌ Config file not found: {self.config_file}")
            print("\n📋 Setup Instructions:")
            print("1. Open Telegram, search: @BotFather")
            print("2. Send: /newbot")
            print("3. Name: Polymarket Alerts")
            print("4. Username: polymarket_alerts_bot (or similar)")
            print("5. Save BOT TOKEN")
            print("6. Search your bot in Telegram, send: /start")
            print("7. Get Chat ID:")
            print("   Visit: https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates")
            print("   Find: 'chat':{'id': YOUR_CHAT_ID}")
            print("8. Run: python tools/alerter.py --setup <TOKEN> <CHAT_ID>")
            exit(1)
        except Exception as e:
            print(f"❌ Error loading config: {str(e)}")
            exit(1)
    
    def send_message(self, message, parse_mode='HTML'):
        """
        Send message to Telegram
        
        Args:
            message: Message text (supports HTML/Markdown)
            parse_mode: 'HTML' or 'Markdown'
            
        Returns:
            API response or None if failed
        """
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': parse_mode
            }
            
            response = requests.post(url, json=data, timeout=10)
            result = response.json()
            
            if result.get('ok'):
                print(f"✅ Alert sent successfully")
                return result
            else:
                print(f"❌ Telegram API error: {result}")
                return None
                
        except requests.exceptions.Timeout:
            print(f"❌ Timeout sending alert")
            return None
        except Exception as e:
            print(f"❌ Error sending alert: {str(e)}")
            return None
    
    def send_price_alert(self, market_name, old_prob, new_prob, volume=None):
        """
        Send price movement alert
        
        Args:
            market_name: Market name
            old_prob: Old probability (%)
            new_prob: New probability (%)
            volume: 24h volume (optional)
        """
        change = new_prob - old_prob
        emoji = "📈" if change > 0 else "📉" if change < 0 else "➡️"
        
        # Determine urgency
        if abs(change) >= 10:
            urgency = "🔴 HIGH"
        elif abs(change) >= 5:
            urgency = "🟡 MEDIUM"
        else:
            urgency = "🟢 LOW"
        
        message = f"""
{emoji} <b>POLYMARKET ALERT</b>
{urgency}

<b>Market:</b> {market_name}
<b>Change:</b> {change:+.1f}%
<b>Old:</b> {old_prob:.1f}% → <b>New:</b> {new_prob:.1f}%

{f'<b>Volume:</b> ${volume:,}' if volume else ''}
<b>Time:</b> {datetime.now().strftime('%H:%M:%S')}
        """
        
        print(f"\n{message}")
        return self.send_message(message)
    
    def send_market_opportunity(self, market_name, probability, edge, recommendation):
        """
        Send market opportunity alert
        
        Args:
            market_name: Market name
            probability: Current probability (%)
            edge: Calculated edge (%)
            recommendation: Buy/Sell/Wait
        """
        emoji = "✅" if recommendation == "BUY" else "❌" if recommendation == "SELL" else "⏳"
        
        message = f"""
{emoji} <b>MARKET OPPORTUNITY</b>

<b>Market:</b> {market_name}
<b>Probability:</b> {probability:.1f}%
<b>Edge:</b> {edge:+.1f}%
<b>Recommendation:</b> {recommendation}

<b>Time:</b> {datetime.now().strftime('%H:%M:%S')}
        """
        
        print(f"\n{message}")
        return self.send_message(message)
    
    def send_daily_summary(self, markets_data):
        """
        Send daily summary report
        
        Args:
            markets_data: List of market dictionaries
        """
        message = "📊 <b>DAILY POLYMARKET SUMMARY</b>\n"
        
        for i, market in enumerate(markets_data[:5], 1):  # Top 5 markets
            message += f"{i}. <b>{market['name']}</b>\n"
            message += f"   Probability: {market['probability']:.1f}%\n"
            message += f"   Volume: ${market['volume']:,}\n\n"
        
        message += f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        print(f"\n{message}")
        return self.send_message(message)
    
    def test_connection(self):
        """Test Telegram connection"""
        message = """
✅ <b>Telegram Alert System - Test Successful</b>

Polymarket Intelligence is ready to send alerts!

<b>Bot:</b> @polymarket_alerts_bot
<b>Time:</b> {time}
        """.format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        print("🧪 Testing Telegram connection...")
        return self.send_message(message)


def setup_bot():
    """Interactive bot setup"""
    print("🤖 Telegram Bot Setup")
    print("=" * 60)
    
    token = input("Enter Bot Token (from @BotFather): ").strip()
    chat_id = input("Enter Chat ID: ").strip()
    
    if token and chat_id:
        alerter = TelegramAlerter(bot_token=token, chat_id=chat_id)
        print("\n✅ Setup complete!")
        
        # Test
        test = input("\nSend test message? (y/n): ").strip().lower()
        if test == 'y':
            alerter.test_connection()
    else:
        print("❌ Invalid input")


def main():
    """Example usage"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--setup':
        setup_bot()
        return
    
    print("🚨 Polymarket Alert System - Starting...")
    print("=" * 60)
    
    # Initialize alerter
    try:
        alerter = TelegramAlerter()
    except:
        print("\n❌ Failed to initialize alerter.")
        print("Run: python tools/alerter.py --setup")
        return
    
    # Test connection
    alerter.test_connection()
    
    # Example: Send price alert
    # alerter.send_price_alert(
    #     "Will Iranian regime fall by June 30?",
    #     old_prob=33.0,
    #     new_prob=38.0,
    #     volume=110000
    # )
    
    # Example: Send opportunity
    # alerter.send_market_opportunity(
    #     "BTC > $10K by Dec 2026",
    #     probability=45.0,
    #     edge=+12.0,
    #     recommendation="BUY"
    # )
    
    # Example: Daily summary
    # alerter.send_daily_summary([
    #     {'name': 'Iran Regime Fall', 'probability': 3.0, 'volume': 110000},
    #     {'name': 'BTC $100K', 'probability': 45.0, 'volume': 5000}
    # ])
    
    print("\n" + "=" * 60)
    print("✅ Alert system ready!")
    print("Check your Telegram for test message")
    print("=" * 60)


if __name__ == "__main__":
    main()
