Feature: Crypto.com Exchange REST API - Candlestick Data
  As a trader or developer
  I want to retrieve candlestick data from the exchange
  So that I can analyze price movements and trading patterns

  Background:
    Given the REST API client is initialized

  @smoke @positive
  Scenario Outline: Retrieve candlestick data with valid parameters
    When I request candlestick data for "<instrument>" with timeframe "<timeframe>" and count <count>
    Then the response status should be 200
    And the response should contain valid candlestick data
    And the instrument name should be "<instrument>"
    And the timeframe should be "<timeframe>"
    And the number of candlesticks should be <count> or less
    And each candlestick should have valid OHLC relationships
    And candlesticks should be in chronological order
    And all volumes should be non-negative
    And the response should be received within 5 seconds

    Examples:
      | instrument      | timeframe | count |
      | BTCUSD-PERP     | 1m        | 10    |
      | BTCUSD-PERP     | 5m        | 20    |
      

  @positive
  Scenario: Retrieve candlestick data with time range
    When I request candlestick data for "BTCUSD-PERP" with timeframe "1h" from 24 hour ago to now
    Then the response status should be 200
    And the response should contain valid candlestick data
    

  @negative
  Scenario Outline: Handle invalid parameters gracefully
    When I request candlestick data with invalid parameters "<param_type>"
    Then the response status should be 400 or 422
    And the response should contain an error message

    Examples:
      | param_type           |
      | invalid_instrument   |
      | invalid_timeframe    |


  @performance
  Scenario: Performance test for candlestick endpoint
    When I request candlestick data for "BTCUSD-PERP" with timeframe "1m" and count 100
    Then the response should be received within 3 seconds
    And the response status should be 200
