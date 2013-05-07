Feature: Program resources and relationships

  Background:
    Given service description
    And a new "Program" named "example_program"
    And "example_program" is POSTed to its collection

  Scenario: The program directives are empty
    Given nothing new
    When GET of the resource "example_program"
    Then the "directives" property of the "example_program" is empty

  Scenario: Adding a program directive
    Given a new "Directive" named "example_directive"
    And "example_program" is added to links property "programs" of "example_directive"
    And "example_directive" is POSTed to "/api/directives"
    When GET of the resource "example_program"
    Then the "directives" property of the "example_program" is not empty
    And "example_directive" is in the links property "directives" of "example_program"
