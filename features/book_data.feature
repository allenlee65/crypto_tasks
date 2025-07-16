Feature: Crypto.com Exchange WebSocket API - Order Book Data
  As a trader or developer
  I want to receive real-time order book data via WebSocket
  So that I can monitor market depth and make informed trading decisions

  Background:
    Given the WebSocket client is initialized

  @smoke @positive
  Scenario: Subscribe to order book data with valid instrument and valid depth
    When I connect to the WebSocket server
    Then the connection should be established successfully
    When I subscribe to order book data with valid instrument "instrument" and valid depth "depth"
    Then I should receive subscription confirmation
    
         
  @smoke @postitive
  Scenario: Subscribe to order book.update with valid parameters
    When I connect to the WebSocket server
    Then the connection should be established successfully
    When I subscribe to order book.update with valid "channels" and "book_subscription_type" and "book_update_frequency"
    Then I should receive subscription confirmation
  
  @negative
  Scenario: Handle invalid subscription instrument and valid depth
    When I connect to the WebSocket server
    Then the connection should be established successfully
    When I subscribe to order book with invalid instrument "insturment" and valid depth "depth"
    Then I should receive an error message
    And the error should indicate Unknown symbol

  @negative
  Scenario: Handle valid subscription instrument and invalid depth
    When I connect to the WebSocket server
    Then the connection should be established successfully
    When I subscribe to order book with valid instrument "insturment" and invalid depth "depth"
    Then I should receive an error message
    And the error should indicate Unknown symbol

  @connection
  Scenario: Handle connection lifecycle
    When I connect to the WebSocket server
    Then the connection should be established successfully
    When I disconnect from the WebSocket server
    Then the connection should be closed gracefully

  @performance
  Scenario: Verify real-time data updates
    When I connect to the WebSocket server
    Then the connection should be established successfully
    When I subscribe to order book for instrument "instrument" with depth "depth"
    Then I should receive order book updates within 5 seconds
    And updates should be received continuously
