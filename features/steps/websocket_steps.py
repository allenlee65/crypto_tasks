
import time


# Add project root to path
import sys
import os
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now import your modules
from utils.websocket_client import CryptoWebSocketClient
from utils.data_validators import OrderBookValidator
from config.test_data import test_data

@given('the WebSocket client is initialized')
def step_init_websocket_client(context):
    context.ws_client = CryptoWebSocketClient()

@when('I connect to the WebSocket server')
def step_connect_websocket(context):
    context.connection_result = context.ws_client.connect()

@then('the connection should be established successfully')
def step_verify_connection(context):
    assert context.connection_result, "Failed to establish WebSocket connection"
    assert context.ws_client.connected, "WebSocket client not in connected state"

@when('I subscribe to order book for "{instrument}" with depth {depth:d}')
def step_subscribe_order_book(context, instrument, depth):
    context.subscription_result = context.ws_client.subscribe_to_book(instrument, depth)
    context.subscribed_instrument = instrument
    context.subscribed_depth = depth
    time.sleep(1)  # Wait for subscription to process

@when('I subscribe to order book with invalid parameters "{param_type}"')
def step_subscribe_invalid_parameters(context, param_type):
    invalid_cases = test_data.get_websocket_negative_cases()
    test_case = next((case for case in invalid_cases if case['name'] == param_type), None)
    
    assert test_case, f"Test case {param_type} not found"
    
    context.subscription_result = context.ws_client.subscribe_to_book(
        test_case.get('instrument', 'INVALID'),
        test_case.get('depth', -1)
    )
    time.sleep(1)

@then('I should receive subscription confirmation')
def step_verify_subscription_confirmation(context):
    assert context.subscription_result, "Subscription request failed"
    
    # Wait for confirmation message
    time.sleep(2)
    channel = f"book.{context.subscribed_instrument}.{context.subscribed_depth}"
    assert context.ws_client.is_subscribed(channel), f"No confirmation received for {channel}"

@then('I should receive order book updates for "{instrument}"')
def step_verify_order_book_updates(context, instrument):
    # Wait for order book data
    assert context.ws_client.wait_for_messages(timeout=10), "No messages received"
    
    messages = context.ws_client.get_received_messages()
    book_updates = [msg for msg in messages if 
                msg.get('method') == 'public/book' and 
                instrument in str(msg.get('params', {}))]
    
    assert len(book_updates) > 0, f"No order book updates received for {instrument}"
    context.order_book_data = book_updates

@then('the order book data should have valid structure')
def step_verify_order_book_structure(context):
    for update in context.order_book_data:
        assert OrderBookValidator.validate_order_book_structure(update), \
            "Invalid order book structure"

@then('the bid and ask prices should be in correct order')
def step_verify_bid_ask_order(context):
    for update in context.order_book_data:
        assert OrderBookValidator.validate_bid_ask_order(update), \
            "Bid and ask prices not in correct order"

@then('all price and quantity values should be positive')
def step_verify_positive_values(context):
    for update in context.order_book_data:
        assert OrderBookValidator.validate_positive_values(update), \
            "Found non-positive price or quantity values"

@then('the depth should not exceed {max_depth:d} levels')
def step_verify_depth_limit(context, max_depth):
    for update in context.order_book_data:
        data = update.get('params', {}).get('data', [])
        if data:
            bids = data[0].get('bids', [])
            asks = data[0].get('asks', [])
            
            assert len(bids) <= max_depth, f"Bids depth {len(bids)} exceeds limit {max_depth}"
            assert len(asks) <= max_depth, f"Asks depth {len(asks)} exceeds limit {max_depth}"

@then('I should receive an error message')
def step_verify_error_message(context):
    messages = context.ws_client.get_received_messages()
    error_messages = [msg for msg in messages if 'Unknown symbol' in msg]
    
    assert len(error_messages) > 0, "No error message received"

@then('the error should indicate invalid parameters')
def step_verify_invalid_parameters_error(context):
    messages = context.ws_client.get_received_messages()
    error_messages = [msg for msg in messages if 'Unknown' in msg or 'error' in msg]

    assert any('Unknown symbol' in str(msg).lower() or 'error' in str(msg).lower() or 'parameter' in str(msg).lower()
            for msg in error_messages), "Error message doesn't indicate invalid parameters"

@when('I disconnect from the WebSocket server')
def step_disconnect_websocket(context):
    context.ws_client.disconnect()

@then('the connection should be closed gracefully')
def step_verify_disconnection(context):
    time.sleep(1)
    assert not context.ws_client.connected, "WebSocket still connected after disconnect"

@then('I should receive order book updates within {seconds:d} seconds')
def step_verify_timely_updates(context, seconds):
    assert context.ws_client.wait_for_messages(timeout=seconds), \
        f"No messages received within {seconds} seconds"

@then('updates should be received continuously')
def step_verify_continuous_updates(context):
    initial_count = len(context.ws_client.get_received_messages())
    time.sleep(3)
    final_count = len(context.ws_client.get_received_messages())
    
    assert final_count > initial_count, "No continuous updates received"
