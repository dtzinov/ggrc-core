Feature: Many resources can be "categorized". This feature will exercise
  categorizing relations.

  Background:
    Given service description

  @wip
  Scenario Outline:
    Given a Category resource named "some_category" for scope "<scope>"
    And "some_category" is POSTed to its collection
    And a new "<resource_type>" named "categorized_resource"
    And "some_category" is added to links property "<category_property>" of "categorized_resource"
    And "categorized_resource" is POSTed to its collection
    When GET of the resource "some_category"
    And GET of the resource "some_category"
    Then the "<category_property>" property of the "categorized_resource" is not empty
    And "some_category" is in the links property "<category_property>" of "categorized_resource"
    And the "<categorizable_property>" property of the "some_category" is not empty
    And "categorized_resource" is in the links property "<categorizable_property>" of "some_category"

  Examples:
      | resource_type | category_property | categorizable_property | scope |
      | Control       | categories        | controls               | 100   |
      | Control       | assertions        | controls               | 102   |
      | Risk          | categories        | risks                  | 100   |

