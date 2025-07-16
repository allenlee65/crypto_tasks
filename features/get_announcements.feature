Feature: Fetch announcements from Crypto.com Exchange

  Scenario Outline: Get announcements with category and product_type filters
    Given the API endpoint is set to "https://api.crypto.com/v1/public/get-announcements"
    When I send a GET request with category "category" and product_type "product_type"
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
