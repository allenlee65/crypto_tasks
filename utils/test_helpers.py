import time
import json
import logging
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
import requests
from config.settings import config

logger = logging.getLogger(__name__)

class TestHelpers:
    """General test helper utilities"""
    
    @staticmethod
    def wait_for_condition(condition_func: Callable[[], bool],
                        timeout: int = 10,
                        interval: float = 0.1,
                        error_message: str = "Condition not met within timeout") -> bool:
        """
        Wait for a condition to be true within timeout
        
        Args:
            condition_func: Function that returns bool
            timeout: Maximum time to wait in seconds
            interval: Check interval in seconds
            error_message: Error message if timeout occurs
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                if condition_func():
                    return True
            except Exception as e:
                logger.debug(f"Condition check failed: {e}")
            
            time.sleep(interval)
        
        logger.error(f"{error_message} (timeout: {timeout}s)")
        return False
    
    @staticmethod
    def retry_operation(operation: Callable,
                    max_retries: int = 3,
                    delay: float = 1.0,
                    exceptions: tuple = (Exception,)) -> Any:
        """
        Retry an operation with exponential backoff
        
        Args:
            operation: Function to retry
            max_retries: Maximum number of retry attempts
            delay: Initial delay between retries
            exceptions: Tuple of exceptions to catch and retry
        """
        for attempt in range(max_retries + 1):
            try:
                return operation()
            except exceptions as e:
                if attempt == max_retries:
                    logger.error(f"Operation failed after {max_retries} retries: {e}")
                    raise
                
                wait_time = delay * (2 ** attempt)  # Exponential backoff
                logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
    
    @staticmethod
    def generate_timestamp(offset_hours: int = 0) -> int:
        """Generate timestamp in milliseconds with optional offset"""
        dt = datetime.now() + timedelta(hours=offset_hours)
        return int(dt.timestamp() * 1000)
    
    @staticmethod
    def format_currency_pair(base: str, quote: str) -> str:
        """Format currency pair for API calls"""
        return f"{base.upper()}_{quote.upper()}"
    
    @staticmethod
    def validate_response_time(start_time: float, max_response_time: float = 5.0) -> bool:
        """Validate API response time"""
        response_time = time.time() - start_time
        return response_time <= max_response_time

class CandlestickHelpers:
    """Helpers specific to candlestick data testing"""
    
    @staticmethod
    def validate_ohlc_logic(open_price: float, high: float, low: float, close_price: float) -> bool:
        """Validate OHLC price relationships"""
        try:
            # High should be >= max(open, close)
            if high < max(open_price, close_price):
                return False
            
            # Low should be <= min(open, close)
            if low > min(open_price, close_price):
                return False
            
            # All prices should be positive
            if any(price <= 0 for price in [open_price, high, low, close_price]):
                return False
            
            return True
        except (TypeError, ValueError):
            return False
    
    @staticmethod
    def calculate_price_change(open_price: float, close_price: float) -> Dict[str, float]:
        """Calculate price change metrics"""
        try:
            change = close_price - open_price
            change_percent = (change / open_price) * 100 if open_price != 0 else 0
            
            return {
                'change': change,
                'change_percent': change_percent,
                'is_bullish': change > 0,
                'is_bearish': change < 0
            }
        except (TypeError, ValueError, ZeroDivisionError):
            return {'change': 0, 'change_percent': 0, 'is_bullish': False, 'is_bearish': False}
    
    @staticmethod
    def validate_chronological_order(candlesticks: List[Dict]) -> bool:
        """Validate that candlesticks are in chronological order"""
        if len(candlesticks) < 2:
            return True
        
        for i in range(1, len(candlesticks)):
            if candlesticks[i]['t'] <= candlesticks[i-1]['t']:
                return False
        return True
    
    @staticmethod
    def get_timeframe_duration_ms(timeframe: str) -> int:
        """Get timeframe duration in milliseconds"""
        timeframe_map = {
            '1m': 60 * 1000,
            '5m': 5 * 60 * 1000,
            '15m': 15 * 60 * 1000,
            '30m': 30 * 60 * 1000,
            '1h': 60 * 60 * 1000,
            '4h': 4 * 60 * 60 * 1000,
            '6h': 6 * 60 * 60 * 1000,
            '12h': 12 * 60 * 60 * 1000,
            '1D': 24 * 60 * 60 * 1000,
            '7D': 7 * 24 * 60 * 60 * 1000,
            '14D': 14 * 24 * 60 * 60 * 1000,
            '1M': 30 * 24 * 60 * 60 * 1000  # Approximate
        }
        return timeframe_map.get(timeframe, 0)

class BookHelpers:
    """Helpers specific to order book testing"""
    
    @staticmethod
    def validate_price_levels(levels: List[List], ascending: bool = True) -> bool:
        """Validate price level ordering"""
        if len(levels) < 2:
            return True
        
        for i in range(1, len(levels)):
            try:
                current_price = float(levels[i][0])
                previous_price = float(levels[i-1][0])
                
                if ascending:
                    if current_price <= previous_price:
                        return False
                else:
                    if current_price >= previous_price:
                        return False
            except (ValueError, IndexError):
                return False
        
        return True
    
    @staticmethod
    def calculate_spread(bids: List[List], asks: List[List]) -> Dict[str, float]:
        """Calculate bid-ask spread metrics"""
        try:
            if not bids or not asks:
                return {'spread': 0, 'spread_percent': 0, 'mid_price': 0}
            
            best_bid = float(bids[0][0])
            best_ask = float(asks[0][0])
            
            spread = best_ask - best_bid
            mid_price = (best_bid + best_ask) / 2
            spread_percent = (spread / mid_price) * 100 if mid_price != 0 else 0
            
            return {
                'spread': spread,
                'spread_percent': spread_percent,
                'mid_price': mid_price,
                'best_bid': best_bid,
                'best_ask': best_ask
            }
        except (ValueError, IndexError, ZeroDivisionError):
            return {'spread': 0, 'spread_percent': 0, 'mid_price': 0}
    
    @staticmethod
    def validate_level_format(level: List) -> bool:
        """Validate individual price level format [price, quantity, count]"""
        try:
            if not isinstance(level, list) or len(level) != 3:
                return False
            
            price = float(level[0])
            quantity = float(level[1])
            count = int(level[2])
            
            return price > 0 and quantity > 0 and count > 0
        except (ValueError, TypeError, IndexError):
            return False
    
    @staticmethod
    def get_total_volume(levels: List[List]) -> float:
        """Calculate total volume from price levels"""
        try:
            return sum(float(level[1]) for level in levels)
        except (ValueError, IndexError):
            return 0.0

class WebSocketHelpers:
    """Helpers for WebSocket testing"""
    
    @staticmethod
    def wait_for_websocket_message(messages: List[Dict],
                                condition: Callable[[Dict], bool],
                                timeout: int = 10) -> Optional[Dict]:
        """Wait for a specific WebSocket message matching condition"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            for message in reversed(messages):  # Check newest first
                if condition(message):
                    return message
            time.sleep(0.1)
        
        return None
    
    @staticmethod
    def filter_messages_by_channel(messages: List[Dict], channel: str) -> List[Dict]:
        """Filter messages by WebSocket channel"""
        filtered = []
        for msg in messages:
            data = msg.get('data', {})
            if (data.get('result', {}).get('channel') == channel or
                data.get('params', {}).get('channel') == channel):
                filtered.append(msg)
        return filtered
    
    @staticmethod
    def validate_websocket_message_structure(message: Dict, required_fields: List[str]) -> bool:
        """Validate WebSocket message has required fields"""
        try:
            data = message.get('data', {})
            for field in required_fields:
                if field not in data:
                    return False
            return True
        except (TypeError, AttributeError):
            return False

class APITestHelpers:
    """Helpers for API testing"""
    
    @staticmethod
    def make_request_with_retry(method: str, url: str, **kwargs) -> requests.Response:
        """Make HTTP request with retry logic"""
        def make_request():
            return requests.request(method, url, timeout=config.rest_timeout, **kwargs)
        
        return TestHelpers.retry_operation(
            make_request,
            max_retries=config.max_retries,
            delay=config.retry_delay,
            exceptions=(requests.RequestException,)
        )
    
    @staticmethod
    def validate_api_response_structure(response: requests.Response,
                                    required_fields: List[str]) -> bool:
        """Validate API response has required fields"""
        try:
            if response.status_code != 200:
                return False
            
            data = response.json()
            for field in required_fields:
                if field not in data:
                    return False
            return True
        except (json.JSONDecodeError, KeyError):
            return False
    
    @staticmethod
    def log_api_call(method: str, url: str, params: Dict = None,
                    response: requests.Response = None):
        """Log API call details for debugging"""
        logger.info(f"API Call: {method} {url}")
        if params:
            logger.info(f"Parameters: {params}")
        if response:
            logger.info(f"Response Status: {response.status_code}")
            logger.info(f"Response Time: {response.elapsed.total_seconds():.2f}s")

class DataGenerators:
    """Generate test data for various scenarios"""
    
    @staticmethod
    def generate_time_ranges(hours_back: int = 24) -> List[Dict[str, int]]:
        """Generate various time ranges for testing"""
        now = datetime.now()
        ranges = []
        
        # Last hour
        ranges.append({
            'name': 'last_hour',
            'start_ts': int((now - timedelta(hours=1)).timestamp() * 1000),
            'end_ts': int(now.timestamp() * 1000)
        })
        
        # Last 6 hours
        ranges.append({
            'name': 'last_6_hours',
            'start_ts': int((now - timedelta(hours=6)).timestamp() * 1000),
            'end_ts': int(now.timestamp() * 1000)
        })
        
        # Last 24 hours
        ranges.append({
            'name': 'last_24_hours',
            'start_ts': int((now - timedelta(hours=24)).timestamp() * 1000),
            'end_ts': int(now.timestamp() * 1000)
        })
        
        return ranges
    
    @staticmethod
    def generate_invalid_parameters() -> List[Dict[str, Any]]:
        """Generate invalid parameter combinations for negative testing"""
        return [
            {'instrument_name': '', 'timeframe': '1h'},
            {'instrument_name': 'INVALID_PAIR', 'timeframe': '1h'},
            {'instrument_name': 'BTC_USDT', 'timeframe': '2h'},  # Invalid timeframe
            {'instrument_name': 'BTC_USDT', 'timeframe': '1h', 'count': -1},
            {'instrument_name': 'BTC_USDT', 'timeframe': '1h', 'count': 1000},  # Too large
            {'instrument_name': 'BTC_USDT', 'timeframe': '1h', 'start_ts': 'invalid'},
        ]

# Export commonly used helpers
def wait_for_condition(condition_func: Callable[[], bool], timeout: int = 10) -> bool:
    """Convenience function for waiting for conditions"""
    return TestHelpers.wait_for_condition(condition_func, timeout)

def validate_ohlc(open_price: float, high: float, low: float, close_price: float) -> bool:
    """Convenience function for OHLC validation"""
    return CandlestickHelpers.validate_ohlc_logic(open_price, high, low, close_price)

def calculate_spread(bids: List[List], asks: List[List]) -> Dict[str, float]:
    """Convenience function for spread calculation"""
    return BookHelpers.calculate_spread(bids, asks)
