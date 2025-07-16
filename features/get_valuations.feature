Feature: Fetch public valuation data for a given instrument

  Scenario: Successfully fetch index_price valuations for BTCUSD-INDEX
    Given the public API is setup
    When I request "index_price" valuations for instrument "BTCUSD-INDEX" with count 1
    Then the response status code should be 200
    And the response method should be "public/get-valuations"
    And the response should contain instrument name "BTCUSD-INDEX"
    And the response should contain data with value and timestamp
