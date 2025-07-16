Feature: Public Get Trades API

  Scenario: Retrieve the last 5 trades for a specific instrument
    Given the instrument name is "BTCUSD-PERP"
    And the trade count is 5
    When I request the public trades from the API
    Then the response status code should be 200
    And the response method should be "public/get-trades"
    And the result should contain a list of 5 trades
    And each trade should have valid attributes
