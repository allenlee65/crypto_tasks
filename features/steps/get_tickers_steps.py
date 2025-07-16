import requests
from behave import given, when, then
from jsonschema import validate
import time

# base_url = "https://uat-api.3ona.co/exchange/v1/public" 
# Define a basic expected schema (You can expand this as needed)
ticker_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "method": {"type": "string"},
        "code": {"type": "number"},
        "result": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "h": {"type": ["string", "null"]},
                            "l": {"type": ["string", "null"]},
                            "a": {"type": ["string", "null"]},
                            "i": {"type": "string"},
                            "v": {"type": "string"},
                            "vv": {"type": "string"},
                            "oi": {"type": "string"},
                            "c": {"type": ["string", "null"]},
                            "b": {"type": ["string", "null"]},
                            "k": {"type": ["string", "null"]},
                            "t": {"type": "number"}
                        },
                        "required": ["i", "t"]
                    }
                }
            }
        }
    }
}

@given('the public API is running at "{base_url}"')
def step_impl_given_api(context, base_url):
    
    context.base_url = base_url

@when('I request the ticker for instrument "{instrument}"')
def step_impl_when_request(context, instrument):
    context.base_url = "https://uat-api.3ona.co/exchange/v1"
    context.response = requests.get(f'{context.base_url}/public/get-tickers?instrument_name={instrument}')
    context.response_json = context.response.json()

@then('the response method should be "public/get-tickers"')
def step_impl_then_method(context):
    assert context.response_json["method"] == "public/get-tickers", "Unexpected method in response"

@then('the response should contain instrument "{instrument}"')
def step_impl_then_instrument(context, instrument):
    tickers = context.response_json["result"]["data"]
    assert any(ticker["i"] == instrument for ticker in tickers), f"{instrument} not found in tickers data"

@then('the response should contain expected ticker fields')
def step_impl_then_fields(context):
    # Validate against the schema
    validate(instance=context.response_json, schema=ticker_schema)

    # Additional check for the presence and type of usual fields
    ticker = context.response_json["result"]["data"][0]
    assert isinstance(ticker["t"], int), "Timestamp should be an integer"
    assert "v" in ticker, "Volume field missing"
    assert "vv" in ticker, "Volume value field missing"
