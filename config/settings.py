import os
from dataclasses import dataclass

@dataclass
class Config:
    # API Endpoints
    rest_base_url: str = "https://uat-api.3ona.co/exchange/v1/"
    websocket_url: str = "wss://uat-stream.3ona.co/exchange/v1/market"
    
    # Timeouts
    rest_timeout: int = 30
    websocket_timeout: int = 10
    
    # Test Configuration
    max_response_time: int = 5
    default_test_count: int = 10
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Create global config instance
config = Config()

# Override with environment variables if present
config.rest_base_url = os.getenv('CRYPTO_REST_URL', config.rest_base_url)
config.websocket_url = os.getenv('CRYPTO_WS_URL', config.websocket_url)
config.rest_timeout = int(os.getenv('REST_TIMEOUT', config.rest_timeout))

