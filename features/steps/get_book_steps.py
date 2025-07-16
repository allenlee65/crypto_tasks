import requests
from behave import given, when, then

BASE_URL = "https://uat-api.3ona.co/exchange/v1/public/get-book"  # Replace with actual base URL

@given('the instrument name is "{instrument_name}"')
def step_instrument_name(context, instrument_name):
    context.instrument_name = instrument_name

@given('the depth is up to "50"')
def step_depth(context, depth="1"):
    """
    Set the depth for the order book request.
    If depth is not specified, default to 50.
    """
    # If depth is provided in the step, use it; otherwise, default to 50
    if hasattr(context, 'depth'):
        return
    if depth.isdigit():
        context.depth = int(depth)
    else:
        context.depth = 50  # Default to 50 if not specified
    
@when('I request the order book from the public API')
def step_order_book(context):
    params = {
        "instrument_name": context.instrument_name,
        "depth": context.depth
    }
    response = requests.get(BASE_URL, params=params)
    context.response = response
    context.json = response.json()

@then('the method should be "public/get-book"')
def step_method(context):
    assert context.json.get("method") == "public/get-book"

@then('the instrument_name in result should be "{expected_instrument_name}"')
def step_assert_instrument_name(context, expected_instrument_name):
    assert context.json['result']['instrument_name'] == expected_instrument_name


@then('the result should contain a "data" field')
def step_data_field_exists(context):
    assert 'data' in context.json['result']


@then('each bid and ask entry should have 3 valid fields: price, quantity, orders')
def step_data_field(context):
    data = context.json['result']['data'][0]
    for entry in data['bids'] + data['asks']:
        assert len(entry) == 3
        price, qty, orders = entry
        assert isinstance(price, str)
        assert isinstance(qty, str)
        assert isinstance(orders, str)
        # Optional: validate convertible to float
        float(price)
        float(qty)
        int(orders)
