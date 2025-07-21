from behave import given, when, then
import requests

@given('the API endpoint is set to "{endpoint}"')
def step_given_api_endpoint(context, endpoint):
    context.endpoint = endpoint

@when('I send a GET request with category "{category}" and product_type "{product_type}"')
def step_when_send_get_request(context, category, product_type):
    params = {}
    if category:
        params['category'] = category
    if product_type:
        params['product_type'] = product_type
    context.response = requests.get(context.endpoint, params=params)
            
@when('I test all combinations of category and product_type')
def step_when_test_all_combinations(context):
    categories = ['list', 'delist', 'event', 'product', 'system']
    product_types = ['Spot', 'Derivative', 'OTC', 'Staking', 'TradingArena']
    for category in categories:
        for product_type in product_types:
            params = {
                'category': category,
                'product_type': product_type
            }
            context.response = requests.get(context.endpoint, params=params)
            assert context.response.status_code == 200, f"Failed with {category}, {product_type}: status {context.response.status_code}"


@then('the response status code should be 200')
def step_then_status_code_200(context):
    assert context.response.status_code == 200, f"Expected status code 200 but got {context.response.status_code}"

@then('the response should contain a list of announcements')
def step_then_response_contains_list(context):
    json_response = context.response.json()
    assert 'result' in json_response and 'data' in json_response['result'], "Response JSON does not contain 'result.data'"
    assert isinstance(json_response['result']['data'], list), "'result.data' is not a list"

@then('each announcement should have required fields')
def step_then_check_required_fields(context):
    required_fields = ['id', 'category', 'product_type', 'announced_at', 'title', 'content']
    json_response = context.response.json()
    assert 'result' in json_response and 'data' in json_response['result'], "Response JSON does not contain 'result.data'"
    announcements = json_response['result']['data']
    assert isinstance(announcements, list), "'result.data' is not a list"
    for announcement in announcements:
        for field in required_fields:
            assert field in announcement, f"Field '{field}' missing in announcement"


@then('the response should indicate rejection or empty result')
def step_response_reject_or_empty(context):
    resp_json = context.response.json()
    # Adjust assertions to system behavior—either error code or empty data
    assert context.response.status_code in [200, 400, 422], "Unexpected status code"
    if context.response.status_code == 200:
        # Expect 'data' to be empty for unknown filters
        data = resp_json.get('result', {}).get('data', None)
        assert data == [] or data is None, "Expected empty result for invalid params"
    else:
        # Alternatively, expect error message or code in error responses
        assert 'code' in resp_json and resp_json['code'] != 0, "No error code for invalid params"

