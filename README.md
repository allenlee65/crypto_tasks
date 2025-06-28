
# Framework Stracture

crypto_exchange_automation/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   └── test_data.py
├── features/
│   ├── steps/
│   │   ├── __init__.py
│   │   ├── rest_api_steps.py
│   │   └── websocket_steps.py
│   ├── book_subscription.feature
│   ├── candlestick.feature
│   └── environment.py
├── utils/
│   ├── __init__.py
│   ├── data_validators.py
│   ├── rest_client.py
│   ├── websocket_client.py
│   └── test_helpers.py
│── __init__.py
├── behave.ini
├── README.md
└── requirements.txt

## Run all tests

behave

## Run only smoke tests

behave --tags @smoke

## Run only REST API tests

behave --tags @rest

## Run only WebSocket tests

behave --tags @websocket

## Run specific feature

behave features\candlestick

## Run with JSON format

behave --format json

## Run negative tests only

behave --tags @negative
