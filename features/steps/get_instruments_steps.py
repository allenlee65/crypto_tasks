import requests
from behave import when, then
import json

BASE_URL = "https://uat-api.3ona.co/exchange/v1/public/get-instruments"  

@when('I request the list of supported instruments from the public API')
def step_request_instruments(context):
    response = requests.get(BASE_URL)
    context.response = response
    context.json = response.json()

@then('the "method" should be "public/get-instruments"')
def step_method(context):
    assert context.json.get("method") == "public/get-instruments"

@then('the result data should include at least one instrument')
def step_result(context):
    data = context.json.get("result", {}).get("data", [])
    assert isinstance(data, list)
    assert len(data) > 0

@then('each instrument in result data should have valid attributes')
def step_vaild_attributes(context):
    data = context.json.get("result", {}).get("data", [])
    required_fields = [
        "symbol", "inst_type", "display_name", "base_ccy", "quote_ccy",
        "quote_decimals", "quantity_decimals", "price_tick_size",
        "qty_tick_size", "max_leverage", "tradable",
        "expiry_timestamp_ms"
        #"underlying_symbol"
    ]
    for instrument in data:
        for field in required_fields:
            assert field in instrument, f"Missing required field '{field}' in instrument {instrument.get('symbol')}"
        # Additional checks for specific fields
        assert isinstance(instrument.get("symbol"), str), "Symbol should be a string"
        assert isinstance(instrument.get("inst_type"), str), "Instrument type should be a string"
        assert isinstance(instrument.get("tradable"), bool), "Tradable should be a boolean"
        if instrument.get("expiry_timestamp_ms"):
            assert isinstance(instrument.get("expiry_timestamp_ms"), int), "Expiry timestamp should be an integer"
        if instrument.get("underlying_symbol"):
            assert isinstance(instrument.get("underlying_symbol"), str), "Underlying symbol should be a string"
        if instrument.get("max_leverage"):
            assert isinstance(instrument.get("max_leverage"), str), "Max leverage should be a string"