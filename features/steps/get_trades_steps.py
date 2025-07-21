from behave import *
import requests


BASE_URL = "https://uat-api.3ona.co/exchange/v1/public/get-trades"  # Replace with actual base URL

@given('the trade count is {count:d}')
def step_trade_account(context, count):
    context.count = count

@when('I request the public trades from the API')
def step_request_trades(context):
    params = {
        "instrument_name": context.instrument_name,
        "count": context.count
    }
    response = requests.get(BASE_URL, params=params)
    context.response = response
    context.json = response.json()

@then('the response method should be "public/get-trades"')
def step_reponse_method(context):
    assert context.json["method"] == "public/get-trades"

@then('the result should contain a list of {expected_count:d} trades')
def step_result_trades(context, expected_count):
    data = context.json["result"]["data"]
    assert isinstance(data, list)
    assert len(data) <= expected_count

@then('each trade should have valid attributes')
def step_trade_valid_attributes(context):
    trades = context.json["result"]["data"]
    required_fields = {"d", "t", "tn", "q", "p", "s", "i", "m"}

    for trade in trades:
        assert required_fields.issubset(set(trade.keys()))
        assert isinstance(trade["d"], str)
        assert isinstance(trade["t"], int)
        assert isinstance(trade["tn"], int or str)
        assert isinstance(trade["q"], str)
        assert isinstance(trade["p"], str)
        assert isinstance(trade["s"], str)
        assert trade["i"] == context.instrument_name
        assert isinstance(trade["m"], str)
