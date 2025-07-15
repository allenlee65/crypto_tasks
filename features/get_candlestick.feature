Feature: Retrieve candlestick data

Scenario Outline: Get candlestick data for all instrument and timeframe combinations
  Given the API endpoint is set
  When I request candlestick data for instrument "<instrument>" and timeframe "<timeframe>"
  Then the response code should be 0
  And the response should contain candlestick data

Examples:
  | instrument     | timeframe |
  | BTCUSD-PERP    | M1        |
  | BTCUSD-PERP    | M1        |
  | BTCUSD-PERP    | M5        |
  | BTCUSD-PERP    | M5        |
  | ETHUSD-PERP    | M15       |
  | ETHUSD-PERP    | M1        |

