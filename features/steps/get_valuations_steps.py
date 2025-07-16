import requests
from behave import given, when, then
from jsonschema import validate


valuation_schema = {
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
                            "v": {"type": "string"},
                            "t": {"type": "number"}
                        },
                        "required": ["v", "t"]
                    }
                },
                "instrument_name": {"type": "string"}
            },
            "required": ["data", "instrument_name"]
        }
    },
    "required": ["id", "method", "code", "result"]
}

@given('the public API is setup')
def step_given_public_api(context):
    base_url = "https://uat-api.3ona.co/exchange/v1"
    context.base_url = base_url

@when('I request "{valuation_type}" valuations for instrument "{instrument}" with count {count}')
def step_when_request_valuation(context, valuation_type, instrument, count):
    url = f"{context.base_url}/public/get-valuations"
    params = {
        "instrument_name": instrument,
        "valuation_type": valuation_type,
        "count": count
    }
    context.response = requests.get(url, params=params)
    context.response_json = context.response.json()


@then('the response method should be "public/get-valuations"')
def step_then_method_check(context):
    assert context.response_json.get("method") == "public/get-valuations", \
        f"Expected method 'public/get-valuations', got {context.response_json.get('method')}"

@then('the response should contain instrument name "{instrument}"')
def step_then_check_instrument(context, instrument):
    assert context.response_json["result"]["instrument_name"] == instrument, \
        f"Expected instrument '{instrument}', got {context.response_json['result']['instrument_name']}"

@then('the response should contain data with value and timestamp')
def step_then_validate_data_fields(context):
    validate(instance=context.response_json, schema=valuation_schema)
    data = context.response_json["result"]["data"]
    assert data, "No data entries returned"
    first_entry = data[0]
    assert "v" in first_entry and isinstance(first_entry["v"], str), "'v' not found or not a string"
    assert "t" in first_entry and isinstance(first_entry["t"], int), "'t' not found or not an integer"
