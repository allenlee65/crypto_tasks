import time
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.rest_client import CryptoRestClient
from utils.data_validators import CandlestickValidator
from config.test_data import test_data

@given('the REST API client is initialized')
def step_init_rest_client(context):
    context.rest_client = CryptoRestClient()

@when('I request candlestick data for "{instrument}" with timeframe "{timeframe}" and count {count:d}')
def step_request_candlestick_basic(context, instrument, timeframe, count):
    context.start_time = time.time()
    context.response = context.rest_client.get_candlestick(
        instrument_name=instrument,
        timeframe=timeframe,
        count=count
    )
    context.response_time = time.time() - context.start_time

@when('I request candlestick data for "{instrument}" with timeframe "{timeframe}" from {hours:d} hour ago to now')
def step_request_candlestick_time_range(context, instrument, timeframe, hours):
    now = datetime.now()
    start_time = now - timedelta(hours=hours)
    
    context.start_time = time.time()
    context.response = context.rest_client.get_candlestick(
        instrument_name=instrument,
        timeframe=timeframe,
        start_ts=int(start_time.timestamp() * 1000),
        end_ts=int(now.timestamp() * 1000)
    )
    context.response_time = time.time() - context.start_time
    context.time_range_start = start_time
    context.time_range_end = now

@when('I request candlestick data with invalid parameters "{param_type}"')
def step_request_invalid_parameters(context, param_type):
    invalid_cases = test_data.get_negative_test_cases()
    test_case = next((case for case in invalid_cases if case['name'] == param_type), None)
    
    assert test_case, f"Test case {param_type} not found"
    
    context.start_time = time.time()
    context.response = context.rest_client.get_candlestick(
        instrument_name=test_case.get('instrument_name', 'BTC_USDT'),
        timeframe=test_case.get('timeframe', '1h'),
        count=test_case.get('count'),
        start_ts=test_case.get('start_ts')
    )
    context.response_time = time.time() - context.start_time

@then('the response status should be {expected_status:d}')
def step_verify_response_status(context, expected_status):
    assert context.response.status_code == expected_status, \
        f"Expected status {expected_status}, got {context.response.status_code}"

@then('the response status should be {status1:d} or {status2:d}')
def step_verify_response_status_multiple(context, status1, status2):
    actual_status = context.response.status_code
    assert actual_status in [status1, status2], \
        f"Expected status {status1} or {status2}, got {actual_status}"

@then('the response should contain valid candlestick data')
def step_verify_valid_candlestick_data(context):
    assert context.response.status_code == 200, "Response status is not 200"
    
    try:
        response_data = context.response.json()
    except ValueError as e:
        raise AssertionError(f"Response is not valid JSON: {e}")
    
    assert CandlestickValidator.validate_candlestick_response(response_data), \
        "Invalid candlestick response structure"
    
    context.candlestick_data = response_data

@then('the instrument name should be "{expected_instrument}"')
def step_verify_instrument_name(context, expected_instrument):
    result = context.candlestick_data['result']
    assert result['instrument_name'] == expected_instrument, \
        f"Expected instrument {expected_instrument}, got {result['instrument_name']}"

@then('the timeframe should be "{expected_timeframe}"')
def step_verify_timeframe(context, expected_timeframe):
    result = context.candlestick_data['result']
    assert result['interval'] == expected_timeframe, \
        f"Expected timeframe {expected_timeframe}, got {result['interval']}"

@then('the number of candlesticks should be {expected_count:d} or less')
def step_verify_candlestick_count(context, expected_count):
    result = context.candlestick_data['result']
    actual_count = len(result['data'])
    assert actual_count <= expected_count, \
        f"Expected {expected_count} or less candlesticks, got {actual_count}"

@then('all candlesticks should be within the specified time range')
def step_verify_time_range(context):
    result = context.candlestick_data['result']
    start_ts = int(context.time_range_start.timestamp() * 1000)
    end_ts = int(context.time_range_end.timestamp() * 1000)
    
    for candle in result['data']:
        candle_time = candle['t']
        assert start_ts <= candle_time <= end_ts, \
            f"Candlestick timestamp {candle_time} outside range [{start_ts}, {end_ts}]"

@then('each candlestick should have valid OHLC relationships')
def step_verify_ohlc_relationships(context):
    result = context.candlestick_data['result']
    assert CandlestickValidator.validate_candlestick_data_integrity(result['data']), \
        "Candlestick data integrity validation failed"

@then('candlesticks should be in chronological order')
def step_verify_chronological_order(context):
    result = context.candlestick_data['result']
    candlesticks = result['data']
    
    for i in range(1, len(candlesticks)):
        assert candlesticks[i]['t'] > candlesticks[i-1]['t'], \
            f"Candlesticks not in chronological order at index {i}"

@then('all volumes should be non-negative')
def step_verify_positive_volumes(context):
    result = context.candlestick_data['result']
    
    for i, candle in enumerate(result['data']):
        volume = float(candle['v'])
        assert volume >= 0, f"Negative volume at index {i}: {volume}"

@then('the response should contain an error message')
def step_verify_error_message(context):
    try:
        response_data = context.response.json()
        assert 'error' in response_data or context.response.status_code >= 400, \
            "Expected error message in response"
    except ValueError:
        assert context.response.status_code >= 400, \
            "Expected error status code for non-JSON response"

@then('the response should be received within {max_seconds:d} seconds')
def step_verify_response_time(context, max_seconds):
    assert context.response_time <= max_seconds, \
        f"Response time {context.response_time:.2f}s exceeded {max_seconds}s limit"
