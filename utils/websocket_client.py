import websocket
import json
import threading
import time
import logging
from typing import Optional, Dict, Any, List, Union
from config.settings import config

logger = logging.getLogger(__name__)

class CryptoWebSocketClient:
    
    def __init__(self):
        self.ws_url: str = config.websocket_url
        self.ws: Optional[websocket.WebSocketApp] = None
        self.connected: bool = False
        self.connection_error: Optional[str] = None
        self.ws_thread: Optional[threading.Thread] = None
        self.message_handlers: Dict[str, Any] = {}
        self.received_messages: List[Dict[str, Any]] = []
        self.subscription_confirmations: Dict[str, bool] = {}
        
    def connect(self) -> bool:
        """Connect to WebSocket server"""
        try:
            websocket.enableTrace(True)
            
            self.ws = websocket.WebSocketApp(
                self.ws_url,
                on_open=self._on_open,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close
            )
            
            self.connected = False
            self.connection_error = None
            
            self.ws_thread = threading.Thread(
                target=self._run_websocket,
                daemon=True
            )
            self.ws_thread.start()
            
            # Wait for connection with timeout
            timeout = 10
            start_time = time.time()
            
            while not self.connected and not self.connection_error:
                if time.time() - start_time > timeout:
                    logger.error("WebSocket connection timeout")
                    return False
                time.sleep(0.1)
            
            if self.connection_error:
                logger.error(f"WebSocket connection failed: {self.connection_error}")
                return False
                
            logger.info("WebSocket connected successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to WebSocket: {e}")
            return False

    def _run_websocket(self) -> None:
        """Run WebSocket connection"""
        try:
            if self.ws is not None:  # Type guard
                self.ws.run_forever(
                    ping_interval=30,
                    ping_timeout=10
                )
        except Exception as e:
            self.connection_error = str(e)

    def subscribe_to_book(self, instrument_name: str, depth: int) -> bool:
        """
        Subscribe to order book updates
        
        Args:
            instrument_name: Trading pair (e.g., BTCUSDT-PERP)
            depth: Order book depth (10, 50)
        """
        if not self.connected or self.ws is None:  # Type guard
            logger.error("WebSocket not connected")
            return False
            
        channel = f"book.{instrument_name}.{depth}"
        
        subscription_message = {
            "id": int(time.time()),
            "method": "subscribe",
            "params": {
                "channels": [channel]
            }
        }
        
        try:
            self.ws.send(json.dumps(subscription_message))
            logger.info(f"Subscribed to {channel}")
            return True
        except Exception as e:
            logger.error(f"Failed to subscribe to {channel}: {e}")
            return False

    def subscribe_to_book_update(self, channels: str, book_subscription_type: str, book_update_frequency: int) -> bool:
        """
        Subscribe to order book updates with specific parameters
        
        Args:
            channels: Trading pair (e.g., book.BTCUSDT-PERP.10)
            book_subscription_type: Type of subscription (e.g., SNAPSHOT_AND_UPDATE)
            book_update_frequency: Frequency of updates in seconds (e.g., 10, 500)
        """
        if not self.connected or self.ws is None:  # Type guard
            logger.error("WebSocket not connected")
            return False
        
        subscription_message = {
            "id": int(time.time()),
            "method": "subscribe",
            "params": {
                "channels": [channels],
                "book_subscription_type": [book_subscription_type],
                "book_update_frequency": [book_update_frequency]  
            }
        }
        try:
            self.ws.send(json.dumps(subscription_message))
            logger.info(f"Subscribed to {channels} with type {book_subscription_type} and frequency {book_update_frequency}")
            return True
        except Exception as e:
            logger.error(f"Failed to subscribe to {channels}: {e}")
            return False
    
    def unsubscribe_from_book(self, instrument_name: str, depth: int) -> bool:
        """Unsubscribe from order book updates"""
        if not self.connected or self.ws is None:  # Type guard
            logger.error("WebSocket not connected")
            return False
            
        channel = f"book.{instrument_name}.{depth}"
        
        unsubscribe_message = {
            "id": int(time.time()),
            "method": "unsubscribe",
            "params": {
                "channels": [channel]
            }
        }
        
        try:
            self.ws.send(json.dumps(unsubscribe_message))
            logger.info(f"Unsubscribed from {channel}")
            return True
        except Exception as e:
            logger.error(f"Failed to unsubscribe from {channel}: {e}")
            return False

    def disconnect(self) -> None:
        """Disconnect from WebSocket server"""
        if self.ws is not None:  # Type guard
            self.ws.close()
        self.connected = False

    def get_received_messages(self, message_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get received messages, optionally filtered by type"""
        if message_type:
            return [msg for msg in self.received_messages if msg.get('method') == message_type]
        return self.received_messages.copy()

    def clear_received_messages(self) -> None:
        """Clear the received messages buffer"""
        self.received_messages.clear()

    def _on_open(self, ws: websocket.WebSocketApp) -> None:
        """Called when WebSocket connection is opened"""
        self.connected = True
        logger.info("WebSocket connection opened")

    def _on_message(self, ws: websocket.WebSocketApp, message: str) -> None:
        """Called when message is received"""
        try:
            data = json.loads(message)
            self.received_messages.append(data)
            
            # Handle subscription confirmations
            if data.get('method') == 'subscribe':
                channels = data.get('params', {}).get('channels', [])
                if channels:
                    self.subscription_confirmations[channels[0]] = True
            
            logger.debug(f"Received message: {data}")
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse message: {e}")

    def _on_error(self, ws: websocket.WebSocketApp, error: Union[str, Exception]) -> None:
        """Called when WebSocket error occurs"""
        self.connection_error = str(error)
        logger.error(f"WebSocket error: {error}")

    def _on_close(self, ws: websocket.WebSocketApp, close_status_code: Optional[int], close_msg: Optional[str]) -> None:
        """Called when WebSocket connection is closed"""
        self.connected = False
        logger.info(f"WebSocket connection closed: {close_status_code} - {close_msg}")

    def is_subscribed(self, channel: str) -> bool:
        """Check if subscribed to a specific channel"""
        return self.subscription_confirmations.get(channel, False)

    def wait_for_messages(self, timeout: int = 5) -> bool:
        """Wait for messages to be received"""
        start_time = time.time()
        initial_count = len(self.received_messages)
        
        while time.time() - start_time < timeout:
            if len(self.received_messages) > initial_count:
                return True
            time.sleep(0.1)
        
        return False
