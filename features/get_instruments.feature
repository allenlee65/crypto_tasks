Feature: Public Get Instruments API

  Scenario: Retrieve all supported instruments
    When I request the list of supported instruments from the public API
    Then the response status code should be 200
    And the "method" should be "public/get-instruments"
    And the result data should include at least one instrument
    And each instrument in result data should have valid attributes
