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
    announcements = context.response.json()['result']['data']
    for announcement in announcements:
        for field in required_fields:
            assert field in announcement, f"Field '{field}' missing in announcement"
