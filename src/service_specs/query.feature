Feature: Collection filtering via query parameters

  Background:
    Given service description
  
  Scenario Outline: A single query parameter supplied to a collection finds matching resources
    Given a new "<resource_type>" named "resource1"
    And a new "<resource_type>" named "resource2"
    And a new "<resource_type>" named "resource3"
    And "resource1" property "<property_name>" is "<match_value1>"
    And "resource2" property "<property_name>" is "<match_value2>"
    And "resource3" property "<property_name>" is "<match_value3>"
    And "resource1" is POSTed to its collection
    And "resource2" is POSTed to its collection
    And "resource3" is POSTed to its collection
    When Querying "<resource_type>" with "<property_name>=<match_value1>"
    And GET of the resource "resource1"
    And GET of the resource "resource2"
    And GET of the resource "resource3"
    Then "resource1" is in query result
    Then "resource2" is not in query result
    Then "resource3" is not in query result
    When Querying "<resource_type>" with "<property_name>=<match_value2>"
    Then "resource1" is not in query result
    Then "resource2" is in query result
    Then "resource3" is not in query result
    When Querying "<resource_type>" with "<property_name>=<nomatch_value>"
    Then "resource1" is not in query result
    Then "resource2" is not in query result
    Then "resource3" is not in query result

  Examples: Resources
      | resource_type | property_name | match_value1        | match_value2        | match_value3        | nomatch_value       |
      | Category      | name          | category1           | category2           | category3           | none_match          |
      | Category      | scope_id      | 3                   | 2                   | 1                   | 5                   |
      | Help          | slug          | foo                 | bar                 | baz                 | never               |
      | Program       | start_date    | 2013-06-03T00:00:00 | 2013-06-02T00:00:00 | 2013-06-01T00:00:00 | 2013-05-31T00:00:00 |
      | Cycle         | start_at      | 2013-06-03          | 2013-06-02          | 2013-06-01          | 2013-05-31          |

  Scenario: A single boolean query parameter supplied to a collection finds matching resources
    Given a new "Category" named "resource1"
    And a new "Category" named "resource2"
    And "resource1" property "required" is literal "True"
    And "resource2" property "required" is literal "False"
    And "resource1" is POSTed to its collection
    And "resource2" is POSTed to its collection
    When Querying "Category" with "required=True"
    And GET of the resource "resource1"
    And GET of the resource "resource2"
    Then "resource1" is in query result
    Then "resource2" is not in query result
    When Querying "Category" with "required=False"
    Then "resource1" is not in query result
    Then "resource2" is in query result

  Scenario: An invalid boolean query parameter supplied to a collection receives 400
    When Querying "Category" with bad argument "required=random"
    Then a "400" status code is received

  @skip
  Scenario Outline: An invalid query parameter is supplied to a collection receives 400
    When Querying "<resource_type>" with bad argument "<querystring>"
    Then a "400" status code is received

  Examples:
      | resource_type | querystring          |
      | Category      | _update_attrs=foobar |
      | Category      | foobar=baz           |
