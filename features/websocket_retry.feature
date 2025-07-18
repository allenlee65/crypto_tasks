Feature: Websocket Retry

  Scenario: Retry connection on websocket failure
    Given the websocket connection is lost
    When the system attempts to reconnect
    Then the websocket should be reconnected successfully
