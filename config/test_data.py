# -*- coding: utf-8 -*-

class TestData:
    
    @staticmethod
    def get_valid_instruments():
        """Get list of valid trading instruments"""
        return ['BTCUSD-PERP']
    
    @staticmethod
    def get_valid_timeframes():
        """Get list of valid timeframes"""
        return ['M1','M5','M15','M30' 'H1','H2','H4','H12','D1','7D','14D','1M']
    
    @staticmethod
    def get_valid_depths():
        """Get list of valid order book depths"""
        return [10,50]

    @staticmethod
    def get_possitive_test_cases():
        """Get possitive test cases for REST API"""
        return [
            {
                'name': 'valid_instrument',
                'instrument_name': 'BTCUSD-PERP',
                'timeframe': 'M1',
                'count': 10
            },
            {
                'name': 'valid_instrument',
                'instrument_name': 'BTCUSD-PERP',
                'timeframe': 'M5',
                'count': 25
            }
        ]

    @staticmethod
    def get_negative_test_cases():
        """Get negative test cases for REST API"""
        return [
            {
                'name': 'invalid_instrument',
                'instrument_name': 'BTCBTC-INVALID',
                'timeframe': 'H1'
            },
            {
                'name': 'invalid_timeframe',
                'instrument_name': 'BTCUSD-PERP',
                'timeframe': 'M99',
                'count': 10
            },
            {
                'name': 'excessive_count',
                'instrument_name': 'BTCUSD-PERP',
                'timeframe': 'M1',
                'count': -99
            },
            {
                'name': 'invalid_timestamp',
                'instrument_name': 'BTCUSD-PERP',
                'timeframe': 'M1',
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
                'depth': 50,
                'channels':'book.BTCUSD-PERP.50'
            },
            {
                'name': 'valid_unsubscription',
                'instrument': 'BTCUSD-PERP',
                'depth': 10,
                'channels':'book.BTCUSD-PERP.10'
            }
        ]
    
    @staticmethod
    def get_valid_websocket_book_update_cases():
        """Get valid test cases for WebSocket API"""
        return [
            {
                'name': 'valid_subscription_with_book_update_10',
                'channels': 'book.BTCUSD-PERP.10',
                'book_subscription_type': 'SNAPSHOT_AND_UPDATE',
                'book_update_frequency': 10
            },
            {
                'name': 'valid_subscription_with_book_update_500',
                'channels': 'book.BTCUSD-PERP.10',
                'book_subscription_type': 'SNAPSHOT_AND_UPDATE',
                'book_update_frequency': 500
            },
        ]

    @staticmethod
    def get_websocket_negative_cases():
        """Get negative test cases for WebSocket API"""
        return [
            {
                'name': 'invalid_instrument',
                'instrument': 'BTCBTC-INVALID',
                'depth': 10,
                'channels':'book.BTCBTC-INVALID.10'
            },
            {
                'name': 'invalid_depth',
                'instrument': 'BTCUSD-PERP',
                'depth': 999,
                'channels':'book.BTCUSD-PERP.999'
            },
            {
                'name': 'missing_instrument',
                'instrument': '',
                'depth': 10,
                'channels':'book. .10'
            }
        ]




# Create global test data instance
test_data = TestData()
