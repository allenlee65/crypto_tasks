import requests
import time
from typing import Dict, Any, Optional
from config.settings import config
import logging

logger = logging.getLogger(__name__)

class CryptoRestClient:
    
    def __init__(self):
        self.base_url = config.rest_base_url
        self.timeout = config.rest_timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'CryptoExchange-TestFramework/1.0'
        })
    
    def get_candlestick(self, instrument_name: str, timeframe: str,
                count: Optional[int] = None, start_ts: Optional[int] = None,
                end_ts: Optional[int] = None) -> requests.Response:
        """
        Get candlestick data from public/get-candlestick endpoint
        
        Args:
            instrument_name: Trading pair (e.g., BTC_USDT)
            timeframe: Time interval (1m, 5m, 15m, 30m, 1h, 4h, 6h, 12h, 1D, 7D, 14D, 1M)
            count: Number of candlesticks to return (max 300)
            start_ts: Start timestamp in milliseconds
            end_ts: End timestamp in milliseconds
        """
        endpoint = f"{self.base_url}/public/get-candlestick"
        
        params: Dict[str, Any] = {
            "instrument_name": instrument_name,
            "timeframe": timeframe
        }
        
        if count is not None:
            params["count"] = str(count)
        if start_ts is not None:
            params["start_ts"] = str(start_ts)
        if end_ts is not None:
            params["end_ts"] = str(end_ts)
            
        logger.info(f"Making request to {endpoint} with params: {params}")
        
        try:
            response = self.session.get(
                endpoint,
                params=params,
                timeout=self.timeout
            )
            logger.info(f"Response status: {response.status_code}")
            return response
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise
    
    def get_instruments(self) -> requests.Response:
        """Get list of available instruments"""
        endpoint = f"{self.base_url}/public/get-instruments"
        return self.session.get(endpoint, timeout=self.timeout)
    
    def close(self):
        """Close the session"""
        self.session.close()
