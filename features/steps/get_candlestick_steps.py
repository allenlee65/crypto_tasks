import requests
from behave import given, when, then

API_URL = "https://uat-api.3ona.co/exchange/v1/public/get-candlestick"  

@given('the API endpoint is set')
def step_given_api_endpoint(context):
    context.api_url = API_URL

@when('I request candlestick data for instrument "{instrument}" and timeframe "{timeframe}"')
def step_when_request_candlestick(context, instrument, timeframe):
    params = {
        "instrument_name": instrument,
        "timeframe": timeframe
    }
    response = requests.get(context.api_url, params=params)
    context.response = response.json()
    print(context.api_url)
    print(f"Response: {context.response}")

@then('the response code should be 0')
def step_then_response_code(context):
    assert context.response["code"] == 0, f"Expected code 200 but got {context.response['code']}"

@then('the response should contain candlestick data')
def step_then_response_data(context):
    result = context.response.get("result", {})
    assert "data" in result and len(result["data"]) > 0, "No candlestick data found in response"
