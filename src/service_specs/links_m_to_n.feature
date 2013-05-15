Feature: Many resources type pairs reference each other M x N relations. This 
  feature will exercise the cases where the linking between resources is M x N.

  Background:
    Given service description

  Scenario Outline:
    Given a new "<type_a>" named "resource_a"
    And "resource_a" is POSTed to its collection
    And a new "<type_b>" named "resource_b"
    And "resource_a" is added to links property "<link_property_b>" of "resource_b"
    And "resource_b" is POSTed to its collection
    When GET of the resource "resource_a"
    And GET of the resource "resource_b"
    Then the "<link_property_a>" property of the "resource_a" is not empty
    And "resource_b" is in the links property "<link_property_a>" of "resource_a"
    And the "<link_property_b>" property of the "resource_b" is not empty
    And "resource_a" is in the links property "<link_property_b>" of "resource_b"
    # Now, do it the reverse way
    Given a new "<type_b>" named "resource_b"
    And "resource_b" is POSTed to its collection
    Given a new "<type_a>" named "resource_a"
    And "resource_b" is added to links property "<link_property_a>" of "resource_a"
    And "resource_a" is POSTed to its collection
    When GET of the resource "resource_a"
    And GET of the resource "resource_b"
    Then the "<link_property_a>" property of the "resource_a" is not empty
    And "resource_b" is in the links property "<link_property_a>" of "resource_a"
    And the "<link_property_b>" property of the "resource_b" is not empty
    And "resource_a" is in the links property "<link_property_b>" of "resource_b"

   Examples: m-by-n link Resources
      | type_a    | link_property_a      | type_b   | link_property_b       |
     #| Control   | documents            | Document | FIXME no property??   |
     #| Control   | people               | Person   | ??                    |
      | Control   | systems              | System   | controls              |
      | Control   | sections             | Section  | controls              |
      | Control   | implemented_controls | Control  | implementing_controls |
      | Control   | risks                | Risk     | controls              |
      | Directive | programs             | Program  | directives            |
      | System    | sub_systems          | System   | super_systems         |
