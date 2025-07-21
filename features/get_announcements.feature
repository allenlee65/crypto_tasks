Feature: Fetch announcements from Crypto.com Exchange

  Scenario Outline: Get announcements with category and product_type filters
    Given the API endpoint is set to "https://uat-api.3ona.co/exchange/v1/public/get-announcements"
    When I send a GET request with category "<category>" and product_type "<product_type>"
    Then the response status code should be 200
    And the response should contain a list of announcements
    And each announcement should have required fields

    Examples:
      | category | product_type |
      | list     | Spot         |
      | delist   | Derivative   |
      | event    | OTC          |
      | product  | Staking      |
      | system   | TradingArena |


  
  Scenario Outline: API should handle unexpected category and product_type gracefully
    Given the API endpoint is set to "https://uat-api.3ona.co/exchange/v1/public/get-announcements"
    When I send a GET request with category "<category>" and product_type "<product_type>"
    Then the response should indicate rejection or empty result

    Examples:
      | category    | product_type |
      | invalid_cat | Spot         |
      | event       | invalid_prod |
      | !@#         | OTC          |
