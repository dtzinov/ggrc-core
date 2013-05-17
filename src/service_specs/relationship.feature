Feature: A Relationship models a relation between two resources. Relationships
  have direction, can be symmetric, and can have their forward and backward
  traversal labeled with a phrase.

  Background:
    Given service description
    And a RelationshipType "test_asymmetric" forward phrase "test_forward"
    And a symmetric RelationshipType "test_symmetric" forward phrase "test_forward" and backward phrase "test_backward"

  Scenario Outline: Asymmetric relations
    Given a new "<type_a>" named "resource_a"
    And "resource_a" is POSTed to its collection
    And a new "<type_b>" named "resource_b"
    And "resource_b" is POSTed to its collection
    And a new "Relationship" named "relationship"
    And "relationship" link property "source" is "resource_a"
    And "relationship" link property "destination" is "resource_b"
    And "relationship" property "relationship_type_id" is "test_asymmetric"
    And "relationship" is POSTed to its collection
    When GET of the resource "relationship"
    Then the "source" of "relationship" is a link to "resource_a"
    And the "destination" of "relationship" is a link to "resource_b"
    And the "relationship_type_id" property of "relationship" is "test_asymmetric"

  Examples:
      | type_a            | type_b           |
      | Category          | Transaction      |
      | Control           | System           |
      | ControlAssessment | Section          |
      | Cycle             | RiskyAttribute   |
      | DataAsset         | Risk             |
      | Directive         | Response         |
      | Document          | Request          |
      | Facility          | Project          |
      | Market            | Program          |
      | Meeting           | Product          |
      | Option            | PopulationSample |
      | OrgGroup          | Person           |
      | PbcList           | PbcList          |

  Scenario Outline: Symmetric relations
    Given a new "<type_a>" named "resource_a"
    And "resource_a" is POSTed to its collection
    And a new "<type_b>" named "resource_b"
    And "resource_b" is POSTed to its collection
    And a new "Relationship" named "relationship"
    And "relationship" link property "source" is "resource_a"
    And "relationship" link property "destination" is "resource_b"
    And "relationship" property "relationship_type_id" is "test_symmetric"
    And "relationship" is POSTed to its collection
    When GET of the resource "relationship"
    Then the "source" of "relationship" is a link to "resource_a"
    And the "destination" of "relationship" is a link to "resource_b"
    And the "relationship_type_id" property of "relationship" is "test_symmetric"

  Examples:
      | type_a            | type_b           |
      | Category          | Transaction      |
      | Control           | System           |
      | ControlAssessment | Section          |
      | Cycle             | RiskyAttribute   |
      | DataAsset         | Risk             |
      | Directive         | Response         |
      | Document          | Request          |
      | Facility          | Project          |
      | Market            | Program          |
      | Meeting           | Product          |
      | Option            | PopulationSample |
      | OrgGroup          | Person           |
      | PbcList           | PbcList          |

