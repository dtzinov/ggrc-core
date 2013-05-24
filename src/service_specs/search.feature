Feature: Full text search

  Background:
    Given service description

  Scenario: Search finds a document with a matching description
    Given a new "Control" named "control"
    And "control" property "description" is "Let's match on foobar!"
    And "control" is POSTed to its collection
    When fulltext search for "foobar" as "results"
    Then "control" is in the search result "results"

  Scenario: Search doesn't find a document without a matching description
    Given a new "Control" named "control"
    And "control" property "description" is "This shouldn't match at all."
    And "control" is POSTed to its collection
    When fulltext search for "bleargh" as "results"
    Then "control" isn't in the search result "results"

  Scenario: Search can group results by type
    Given the following resources are POSTed:
      | type    | name     | description                             |
      | Control | control1 | A control that should match because 42. |
      | Control | control2 | A control that shouldn't match.         |
      | Cycle   | cycle1   | A cycle that should match because 42.   |
    When fulltext search grouped by type for "42" as "results"
    Then "control1" is in the "Control" group of "results"
    And "control2" isn't in the "Control" group of "results"
    And "cycle1" is in the "Cycle" group of "results"
