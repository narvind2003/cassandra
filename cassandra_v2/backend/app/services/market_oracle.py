import yfinance as yf
from typing import Dict, Optional

class MarketOracle:
    """
    Fetches real-time market data using Yahoo Finance.
    Maps internal commodity names to YF Tickers.
    """
    
    TICKER_MAP = {
        "Crude Oil": "CL=F",
        "Brent Crude": "BZ=F",
        "Natural Gas (LNG)": "NG=F",
        "Thermal Coal": "MTF=F", # Rotterdam Coal Futures (approx)
        "Uranium": "URA", # ETF Proxy
        
        "Gold": "GC=F",
        "Silver": "SI=F",
        "Copper": "HG=F",
        "Platinum": "PL=F",
        "Palladium": "PA=F",
        "Aluminum": "ALI=F",
        "Zinc": "ZNC=F",
        "Lead": "LED=F",
        "Nickel": "TNI=F",
        
        "Wheat": "ZW=F",
        "Corn (Maize)": "ZC=F",
        "Soybeans": "ZS=F",
        "Coffee": "KC=F",
        "Cane Sugar": "SB=F",
        "Cocoa": "CC=F",
        "Cotton": "CT=F",
        "Orange Juice": "OJ=F",
        
        "Beef": "LE=F", # Live Cattle
        "Pork": "HE=F", # Lean Hogs
        
        # Tech / Industrial proxies (using ETFs or major players)
        "Lithium-Ion Battery": "LIT", # Lithium ETF
        "Semiconductors": "SMH", # Semiconductor ETF
        "Rare Earths": "REMX", # Rare Earth ETF
        "Lumber": "LBS=F",
        "Rubber": "JPX=F" # Rubber Futures
    }

    @staticmethod
    def fetch_current_price(commodity_name: str) -> Optional[float]:
        ticker = MarketOracle.TICKER_MAP.get(commodity_name)
        if not ticker:
            return None
            
        try:
            data = yf.Ticker(ticker)
            # Try fast info first
            price = data.fast_info.last_price
            if not price:
                # Fallback to history
                hist = data.history(period="1d")
                if not hist.empty:
                    price = hist["Close"].iloc[-1]
            return price
        except Exception as e:
            print(f"Failed to fetch price for {commodity_name} ({ticker}): {e}")
            return None

    @staticmethod
    def fetch_all_prices() -> Dict[str, float]:
        """Batch fetch (can be slow, use sparingly on startup)"""
        results = {}
        # In a real app, use yf.download for batching
        # For now, simplistic loop to avoid complexity
        for comm, ticker in MarketOracle.TICKER_MAP.items():
            p = MarketOracle.fetch_current_price(comm)
            if p:
                results[comm] = p
        return results
