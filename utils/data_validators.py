import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class CandlestickValidator:
    
    @staticmethod
    def validate_candlestick_response(response_data: Dict[str, Any]) -> bool:
        """Validate candlestick response structure"""
        try:
            # Check basic structure
            assert 'result' in response_data, "Missing 'result' field"
            result = response_data['result']
            
            assert 'data' in result, "Missing 'data' field in result"
            assert 'instrument_name' in result, "Missing 'instrument_name' field"
            assert 'interval' in result, "Missing 'interval' field"
            
            # Validate data array
            data = result['data']
            assert isinstance(data, list), "Data should be a list"
            
            for candle in data:
                assert CandlestickValidator._validate_single_candle(candle), \
                    "Invalid candlestick data"
            
            return True
            
        except (AssertionError, KeyError, TypeError) as e:
            logger.error(f"Candlestick validation failed: {e}")
            return False
    
    @staticmethod
    def _validate_single_candle(candle: Dict[str, Any]) -> bool:
        """Validate single candlestick data"""
        required_fields = ['o', 'h', 'l', 'c', 'v', 't']
        
        for field in required_fields:
            if field not in candle:
                return False
        
        # Validate OHLC relationships
        open_price = float(candle['o'])
        high_price = float(candle['h'])
        low_price = float(candle['l'])
        close_price = float(candle['c'])
        volume = float(candle['v'])
        
        # High should be >= all other prices
        if not (high_price >= open_price and high_price >= close_price and high_price >= low_price):
            return False
        
        # Low should be <= all other prices
        if not (low_price <= open_price and low_price <= close_price and low_price <= high_price):
            return False
        
        # Volume should be non-negative
        if volume < 0:
            return False
        
        return True
    
    @staticmethod
    def validate_candlestick_data_integrity(candlesticks: List[Dict[str, Any]]) -> bool:
        """Validate integrity of candlestick data array"""
        try:
            for candle in candlesticks:
                if not CandlestickValidator._validate_single_candle(candle):
                    return False
            return True
        except Exception as e:
            logger.error(f"Data integrity validation failed: {e}")
            return False

class OrderBookValidator:
    
    @staticmethod
    def validate_order_book_structure(message: Dict[str, Any]) -> bool:
        """Validate order book message structure"""
        try:
            assert 'method' in message, "Missing method field"
            assert 'params' in message, "Missing params field"
            
            params = message['params']
            assert 'channel' in params, "Missing channel field"
            assert 'data' in params, "Missing data field"
            
            data = params['data']
            assert isinstance(data, list), "Data should be a list"
            
            if data:  # If data is not empty
                book_data = data[0]
                assert 'bids' in book_data, "Missing bids field"
                assert 'asks' in book_data, "Missing asks field"
                assert 'instrument_name' in book_data, "Missing instrument_name"
                assert 't' in book_data, "Missing timestamp field"
            
            return True
            
        except (AssertionError, KeyError, TypeError, IndexError) as e:
            logger.error(f"Order book structure validation failed: {e}")
            return False
    
    @staticmethod
    def validate_bid_ask_order(message: Dict[str, Any]) -> bool:
        """Validate that bids are in descending order and asks in ascending order"""
        try:
            data = message['params']['data']
            if not data:
                return True
            
            book_data = data[0]
            bids = book_data.get('bids', [])
            asks = book_data.get('asks', [])
            
            # Validate bids are in descending order (highest price first)
            for i in range(1, len(bids)):
                if float(bids[i][0]) > float(bids[i-1][0]):
                    return False
            
            # Validate asks are in ascending order (lowest price first)
            for i in range(1, len(asks)):
                if float(asks[i][0]) < float(asks[i-1][0]):
                    return False
            
            return True
            
        except (KeyError, TypeError, IndexError, ValueError) as e:
            logger.error(f"Bid/ask order validation failed: {e}")
            return False
    
    @staticmethod
    def validate_positive_values(message: Dict[str, Any]) -> bool:
        """Validate that all prices and quantities are positive"""
        try:
            data = message['params']['data']
            if not data:
                return True
            
            book_data = data[0]
            bids = book_data.get('bids', [])
            asks = book_data.get('asks', [])
            
            # Check all bid prices and quantities
            for bid in bids:
                price, quantity = float(bid[0]), float(bid[1])
                if price <= 0 or quantity <= 0:
                    return False
            
            # Check all ask prices and quantities
            for ask in asks:
                price, quantity = float(ask[0]), float(ask[1])
                if price <= 0 or quantity <= 0:
                    return False
            
            return True
            
        except (KeyError, TypeError, IndexError, ValueError) as e:
            logger.error(f"Positive values validation failed: {e}")
            return False
