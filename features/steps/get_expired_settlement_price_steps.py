import requests
from behave import given, when, then
from jsonschema import validate

settlement_schema = {
    "type": "object",
    "properties": {
        "id": { "type": "number" },
        "method": { "type": "string" },
        "code": { "type": "number" },
        "result": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "i": { "type": "string" },  # Instrument name
                            "x": { "type": "number" },  # Expiration timestamp
                            "v": { "type": "string" },  # Settlement value
                            "t": { "type": "number" }   # Publish timestamp
                        },
                        "required": [ "i", "x", "v", "t" ]
                    }
                }
            },
            "required": ["data"]
        }
    },
    "required": ["id", "method", "code", "result"]
}


@when('I request expired settlement prices with instrument_type "{instrument_type}" and page {page}')
def step_when_request_settlement_data(context, instrument_type, page):
    url = f"{context.base_url}/public/get-expired-settlement-price"
    params = {
        "instrument_type": instrument_type,
        "page": page
    }
    context.response = requests.get(url, params=params)
    context.response_json = context.response.json()

@then('the response method should be "public/get-expired-settlement-price"')
def step_then_response_method(context):
    assert context.response_json.get("method") == "public/get-expired-settlement-price", \
        "Unexpected response method"

@then('the response should contain settlement data with instrument name, expiry, value, and timestamp')
def step_then_validate_data_schema(context):
    validate(instance=context.response_json, schema=settlement_schema)

    data = context.response_json["result"]["data"]
    assert data, "Data array is empty"
    entry = data[0]
    assert isinstance(entry["i"], str), "Instrument name 'i' missing or invalid"
    assert isinstance(entry["x"], int), "Expiry timestamp 'x' missing or invalid"
    assert isinstance(entry["v"], str), "Value 'v' missing or invalid"
    assert isinstance(entry["t"], int), "Timestamp 't' missing or invalid"
