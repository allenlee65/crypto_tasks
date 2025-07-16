Feature: Fetch insurance fund data for a specified currency

  Scenario: Successfully fetch insurance fund balance for USD
    Given the public API is setup
    When I request insurance fund data for instrument "USD" with count 1
    Then the response status code should be 200
    And the response method should be "public/get-insurance"
    And the response should contain instrument name "USD"
    And the response should include insurance data with value and timestamp
