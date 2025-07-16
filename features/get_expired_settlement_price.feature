Feature: Fetch expired settlement prices for futures

  Scenario: Successfully fetch expired settlement price data
    Given the public API is setup
    When I request expired settlement prices with instrument_type "FUTURE" and page 1
    Then the response status code should be 200
    And the response method should be "public/get-expired-settlement-price"
    And the response should contain settlement data with instrument name, expiry, value, and timestamp
