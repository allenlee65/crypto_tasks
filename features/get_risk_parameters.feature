Feature: Fetch risk parameters from Crypto.com Exchange
ters
  Scenario: Get risk parameters
    Given the API endpoint for get-risk-parameters is set to "https://uat-api.3ona.co/exchange/v1/public/get-risk-parameters"
    When I send a GET request to the endpoint
    Then the response status code should be 200
    And the response should have the required root fields
    And base_currency_config should be a list of objects with required or optional fields
