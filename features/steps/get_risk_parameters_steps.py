from behave import given, when, then
import requests

@given('the API endpoint for get-risk-parameters is set to "{endpoint}"')
def step_given_api_endpoint(context, endpoint):
    context.endpoint = endpoint

@when('I send a GET request to the endpoint')
def step_when_send_get_request(context):
    context.response = requests.get(context.endpoint)


@then('the response should have the required root fields')
def step_then_response_root_fields(context):
    json_response = context.response.json()
    for field in ['id', 'method', 'code', 'result']:
        assert field in json_response, f"Missing '{field}' in response root"
    result = json_response['result']
    root_fields = [
        'default_max_product_leverage_for_spot',
        'default_max_product_leverage_for_perps',
        'default_max_product_leverage_for_futures',
        'default_unit_margin_rate',
        'default_collateral_cap',
        'update_timestamp_ms',
        'base_currency_config'
    ]
    for field in root_fields:
        assert field in result, f"Missing '{field}' in result object"
    assert isinstance(result['base_currency_config'], list), "base_currency_config is not a list"

@then('base_currency_config should be a list of objects with required or optional fields')
def step_then_validate_base_currency_config(context):
    required_token_fields = ['instrument_name']
    example_optional_fields = [
        'collateral_cap_notional', 'minimum_haircut', 'max_product_leverage_for_spot',
        'max_product_leverage_for_perps', 'max_product_leverage_for_futures',
        'unit_margin_rate', 'max_short_sell_limit', 'daily_notional_limit',
        'max_order_notional_usd', 'min_order_notional_usd'
    ]
    for item in context.response.json()['result']['base_currency_config']:
        for field in required_token_fields:
            assert field in item, f"Missing required field '{field}' in base_currency_config entry {item.get('instrument_name')}"
        # Check that optional fields, if present, are of number or string (as documented)
        for field in example_optional_fields:
            if field in item:
                assert isinstance(item[field], str) or isinstance(item[field], float) or isinstance(item[field], int), \
                    f"Field '{field}' in base_currency_config entry {item.get('instrument_name')} is not a valid number/string"
