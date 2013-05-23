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

