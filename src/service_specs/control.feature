Feature: Controls Service

  Scenario: HTTP POST and GET
    Given an example control
    When the example control is POSTed
    Then a 201 status code is received
    And the response has a Location header
    And we receive a valid control in the entity body
    And the received control matches the one we posted
