Feature: Retrieve candlestick data

Scenario Outline: Get candlestick data for all instrument and timeframe combinations
  Given the API endpoint is set
  When I request candlestick data for instrument "<instrument>" and timeframe "<timeframe>"
  Then the response code should be 0
  And the response should contain candlestick data

Examples:
  | instrument     | timeframe |
  | BTCUSD-PERP    | M1        |
  | BTCUSD-PERP    | M5        |
  | BTCUSD-PERP    | M15       |
  | BTCUSD-PERP    | M30       |
  | ETHUSD-PERP    | H1        |
  | ETHUSD-PERP    | H2        |
  | ETHUSD-PERP    | H1        |
  | ETHUSD-PERP    | H2        |
  | ETHUSD-PERP    | H4        |
  | ETHUSD-PERP    | H12       |
  | ETHUSD-PERP    | D1        |
  | ETHUSD-PERP    | 7D        |
  | ETHUSD-PERP    | 14D       |
  | ETHUSD-PERP    | 1M        |