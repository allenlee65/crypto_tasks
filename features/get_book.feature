Feature: Public Get Book API

  Scenario: Retrieve the order book for an instrument with depth 10
    Given the instrument name is "BTCUSD-PERP"
    And the depth is up to "50"
    When I request the order book from the public API
    Then the response status code should be 200
    And the method should be "public/get-book"
    And the instrument_name in result should be "BTCUSD-PERP"
    And each bid and ask entry should have 3 valid fields: price, quantity, orders
