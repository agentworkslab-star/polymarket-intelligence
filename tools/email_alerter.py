#!/usr/bin/env python3
"""
📧 Polymarket Email Alerts - FREE Version
Send email alerts alongside Telegram
Author: Agent Claw 🦾
Date: 2026-03-08
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path
import json

class EmailAlerter:
    """Send email alerts"""
    
    def __init__(self, smtp_server, smtp_port, email, password, to_email):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password
        self.to_email = to_email
        self.config_file = Path("config/email_config.json")
    
    def send_alert(self, subject, body):
        """Send email alert"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = self.to_email
            msg['Subject'] = f"[Polymarket] {subject}"
            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            
            text = msg.as_string()
            server.sendmail(self.email, self.to_email, text)
            server.quit()
            
            print(f"✅ Email sent: {subject}")
            return True
            
        except Exception as e:
            print(f"❌ Email failed: {str(e)}")
            return False
    
    def send_price_alert(self, market_name, old_prob, new_prob):
        """Send price movement alert"""
        change = new_prob - old_prob
        emoji = "📈" if change > 0 else "📉"
        
        subject = f"{emoji} Price Alert: {market_name}"
        body = f"""
        <h2>Polymarket Price Alert</h2>
        <p><b>Market:</b> {market_name}</p>
        <p><b>Change:</b> {change:+.1f}%</p>
        <p><b>Old:</b> {old_prob:.1f}% → <b>New:</b> {new_prob:.1f}%</p>
        <p><b>Time:</b> {datetime.now().strftime('%H:%M:%S')}</p>
        """
        
        return self.send_alert(subject, body)


def main():
    """Setup and test"""
    print("📧 Email Alerts Setup")
    print("=" * 60)
    
    # For Gmail:
    # smtp_server = "smtp.gmail.com"
    # smtp_port = 587
    
    email = input("Your email: ")
    password = input("App password: ")
    to_email = input("Send to email: ")
    
    alerter = EmailAlerter("smtp.gmail.com", 587, email, password, to_email)
    alerter.send_alert("Test Alert", "<h2>Test Email from Polymarket</h2>")


if __name__ == "__main__":
    main()