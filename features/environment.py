import logging
import sys
import os
from utils.rest_client import CryptoRestClient
from utils.websocket_client import CryptoWebSocketClient

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def before_all(context):
    """Setup before all tests"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    context.rest_client = CryptoRestClient()
    context.ws_client = CryptoWebSocketClient()

    context.config.setup_logging()

def before_feature(context, feature):
    """Setup before each feature"""
    context.rest_client = CryptoRestClient()
    context.ws_client = CryptoWebSocketClient()
    pass

def before_scenario(context, scenario):
    """Setup before each scenario"""
    # Clean up any existing clients
    if hasattr(context, 'rest_client'):
        context.rest_client.close()
    
    if hasattr(context, 'ws_client'):
        context.ws_client.disconnect()

def after_scenario(context, scenario):
    """Cleanup after each scenario"""
    if hasattr(context, 'rest_client'):
        context.rest_client.close()
        
    if hasattr(context, 'ws_client'):
        context.ws_client.disconnect()

def after_all(context):
    """Cleanup after all tests"""
    if hasattr(context, 'ws_client'):
        context.ws_client.disconnect()
