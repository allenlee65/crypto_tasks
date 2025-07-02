# -*- coding: utf-8 -*-

class TestData:
    
    @staticmethod
    def get_valid_instruments():
        """Get list of valid trading instruments"""
        return ['BTCUSD-PERP']
    
    @staticmethod
    def get_valid_timeframes():
        """Get list of valid timeframes"""
        return ['1m', '5m', '15m']
    
    @staticmethod
    def get_valid_depths():
        """Get list of valid order book depths"""
        return [10]
    
    @staticmethod
    def get_negative_test_cases():
        """Get negative test cases for REST API"""
        return [
            {
                'name': 'invalid_instrument',
                'instrument_name': 'INVALID_PAIR',
                'timeframe': '1h',
                'count': 10
            },
            {
                'name': 'invalid_timeframe',
                'instrument_name': 'BTCUSD-PERP',
                'timeframe': 'invalid',
                'count': 10
            },
            {
                'name': 'excessive_count',
                'instrument_name': 'BTCUSD-PERP',
                'timeframe': '1h',
                'count': 1000
            },
            {
                'name': 'invalid_timestamp',
                'instrument_name': 'BTCUSD-PERP',
                'timeframe': '1h',
                'start_ts': -1
            }
        ]
    
    @staticmethod
    def get_valid_websocket_cases():
        """Get valid test cases for WebSocket API"""
        return [
            {
                'name': 'valid_subscription',
                'instrument': 'BTCUSD-PERP',
                'depth': 10,
                'channels':'book.BTCUSD-PERP.10'
            },
            {
                'name': 'valid_unsubscription',
                'instrument': 'BTCUSD-PERP',
                'depth': 10,
                'channels':'book.BTCUSD-PERP.10'
            }
        ]

    @staticmethod
    def get_websocket_negative_cases():
        """Get negative test cases for WebSocket API"""
        return [
            {
                'name': 'invalid_instrument',
                'instrument': 'INVALID_PAIR',
                'depth': 10,
                'channels':'book.BTCUSD-PERP.10'
            },
            {
                'name': 'invalid_depth',
                'instrument': 'BTCUSD-PERP',
                'depth': 999,
                'channels':'book.BTCUSD-PERP.10'
            },
            {
                'name': 'missing_instrument',
                'instrument': '',
                'depth': 10,
                'channels':'book.BTCUSD-PERP.10'
            }
        ]




# Create global test data instance
test_data = TestData()
