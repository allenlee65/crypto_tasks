Feature: Fetch public ticker data for a given instrument

  Scenario: Successfully fetch public ticker data for BTCUSD-PERP
    Given the API endpoint is set
    When I request the ticker for instrument "BTCUSD-PERP"
    Then the response status code should be 200
    And the response method should be "public/get-tickers"
    And the response should contain instrument "BTCUSD-PERP"
    And the response should contain expected ticker fields
