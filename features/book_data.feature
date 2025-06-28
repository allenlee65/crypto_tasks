Feature: Crypto.com Exchange WebSocket API - Order Book Data
  As a trader or developer
  I want to receive real-time order book data via WebSocket
  So that I can monitor market depth and make informed trading decisions

  Background:
    Given the WebSocket client is initialized

  @smoke @positive
  Scenario Outline: Subscribe to order book data with valid parameters
    When I connect to the WebSocket server
    Then the connection should be established successfully
    When I subscribe to order book for "<instrument>" with depth <depth>
    Then I should receive subscription confirmation
    And I should receive order book updates for "<instrument>"
    And the order book data should have valid structure
    And the bid and ask prices should be in correct order
    And all price and quantity values should be positive
    And the depth should not exceed <depth> levels
         
  @negative
  Scenario Outline: Handle invalid subscription parameters
    When I connect to the WebSocket server
    And I subscribe to order book with invalid parameters "<param_type>"
    Then I should receive an error message
    And the error should indicate invalid parameters

  @connection
  Scenario: Handle connection lifecycle
    When I connect to the WebSocket server
    Then the connection should be established successfully
    When I disconnect from the WebSocket server
    Then the connection should be closed gracefully

  @performance
  Scenario: Verify real-time data updates
    When I connect to the WebSocket server
    And I subscribe to order book for "BTCUSD-PERP" with depth 10
    Then I should receive order book updates within 5 seconds
    And updates should be received continuously
