Feature: Many resources have links to other resources. This feature will
  exercise the cases where the linking is n to 1, such as in a child to parent
  relationship.

  Scenario Outline:
    Given a new "<parent_type>" named "parent"
    And "parent" is POSTed to "<parent_collection>"
    And a new "<child_type>" named "child"
    And "child" link property "<parent_property>" is "parent"
    And "child" is POSTed to "<child_collection>"
    When GET of the resource "parent"
    And GET of the resource "child"
    Then the "<parent_property>" of "child" is a link to "parent"
    And "child" is in the links property "<children_property>" of "parent" 

  Examples: Resources
    | parent_type | parent_collection | child_type        | child_collection         | parent_property | children_property   |
    | PbcList     | /api/pbc_lists    | ControlAssessment | /api/control_assessments | pbc_list        | control_assessments |
