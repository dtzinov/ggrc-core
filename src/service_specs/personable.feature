Feature: Some resources can be related to Person resources

  Background:
    Given service description

  Scenario Outline:
    Given a new "Person" named "person"
    And "person" is posted to its collection
    And a new "<personable_type>" named "personable"
    And "person" is added to links property "people" of "personable"
    And "personable" is POSTed to its collection
    When GET of the resource "personable"
    Then "person" is in the links property "people" of "personable"

  Examples:
      | personable_type |
      | Control         |
      | Cycle           |
      | DataAsset       |
      | Directive       |
      | Facility        |
      | Market          |
      | OrgGroup        |
      | Product         |
      | Program         |
      | Project         |
      | Response        |
      | Risk            |
      | RiskyAttribute  |
      | System          |

