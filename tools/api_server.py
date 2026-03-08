#!/usr/bin/env python3
"""
🌐 Polymarket API Server - FREE Version
FastAPI endpoint for data access
Author: Agent Claw 🦾
Date: 2026-03-08
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import json
from datetime import datetime
from pathlib import Path
import glob

app = FastAPI(title="Polymarket Intelligence API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_dir = Path("data/markets")

@app.get("/")
def root():
    """API root"""
    return {
        "name": "Polymarket Intelligence API",
        "version": "1.0",
        "status": "running"
    }

@app.get("/api/markets")
def get_markets():
    """Get all markets"""
    csv_files = glob.glob(str(data_dir / "scrape_*.csv"))
    
    if not csv_files:
        raise HTTPException(status_code=404, detail="No data available")
    
    latest = max(csv_files)
    df = pd.read_csv(latest)
    
    return {
        "count": len(df),
        "timestamp": datetime.now().isoformat(),
        "markets": df.to_dict('records')
    }

@app.get("/api/markets/latest")
def get_latest_market():
    """Get latest market data"""
    csv_files = glob.glob(str(data_dir / "scrape_*.csv"))
    
    if not csv_files:
        raise HTTPException(status_code=404, detail="No data available")
    
    latest = max(csv_files)
    df = pd.read_csv(latest)
    
    return df.iloc[-1].to_dict() if len(df) > 0 else {}

@app.get("/api/predictions")
def get_predictions():
    """Get latest predictions"""
    pred_dir = Path("data/models")
    json_files = glob.glob(str(pred_dir / "predictions_*.json"))
    
    if not json_files:
        raise HTTPException(status_code=404, detail="No predictions available")
    
    latest = max(json_files)
    with open(latest, 'r') as f:
        return json.load(f)

@app.get("/api/status")
def get_status():
    """Get system status"""
    csv_files = glob.glob(str(data_dir / "scrape_*.csv"))
    pred_files = glob.glob(str(Path("data/models") / "predictions_*.json"))
    
    return {
        "status": "healthy",
        "total_scrapes": len(csv_files),
        "total_predictions": len(pred_files),
        "last_scrape": max(csv_files) if csv_files else None,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
