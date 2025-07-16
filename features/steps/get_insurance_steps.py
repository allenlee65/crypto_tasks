import requests
from behave import *
from jsonschema import validate

# JSON schema definition
insurance_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "method": {"type": "string"},
        "code": {"type": "number"},
        "result": {
            "type": "object",
            "properties": {
                "instrument_name": {"type": "string"},
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
                }
            },
            "required": ["instrument_name", "data"]
        }
    },
    "required": ["id", "method", "code", "result"]
}


@when('I request insurance fund data for instrument "{instrument}" with count {count}')
def step_request_insurance_data(context, instrument, count):
    url = f"{context.base_url}/public/get-insurance"
    params = {"instrument_name": instrument, "count": count}
    context.response = requests.get(url, params=params)
    context.response_json = context.response.json()


@then('the response method should be "public/get-insurance"')
def step_check_method(context):
    assert context.response_json.get("method") == "public/get-insurance", \
        f"Unexpected method: {context.response_json.get('method')}"

# @then('the response should contain instrument name "{instrument}"')
# def step_check_instrument_name(context, instrument):
#     actual_instrument = context.response_json["result"]["instrument_name"]
#     assert actual_instrument == instrument, \
#         f"Expected instrument_name '{instrument}', got '{actual_instrument}'"

@then('the response should include insurance data with value and timestamp')
def step_validate_insurance_data_schema(context):
    validate(instance=context.response_json, schema=insurance_schema)
    data = context.response_json["result"]["data"]
    assert data, "No data returned"
    record = data[0]
    assert isinstance(record["v"], str), "'v' should be a string"
    assert isinstance(record["t"], int), "'t' should be an integer"
