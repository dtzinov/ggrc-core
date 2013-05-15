Feature: Options relationships

  Background:
    Given service description

  Scenario Outline:
    Given an Option named "option" with role "<role>"
    And "option" is POSTed to its collection
    And a new "<resource_type>" named "resource"
    And "resource" link property "<link_property>" is "option"
    and "resource" is POSTed to its collection
    When GET of the resource "resource"
    Then the "<link_property>" of "resource" is a link to "option"

  Examples:
      | role             | resource_type | link_property    |
      | control_type     | Control       | type             |
      | control_kind     | Control       | kind             |
      | control_means    | Control       | means            |
      | verify_frequency | Control       | verify_frequency |
      | audit_frequency  | Directive     | audit_frequency  |
      | audit_duration   | Directive     | audit_duration   |
      | document_type    | Document      | type             |
      | reference_type   | Document      | kind             |
      | document_year    | Document      | year             |
      | language         | Document      | language         |
      | person_language  | Person        | language         |
      | product_type     | Product       | type             |
      | system_type      | System        | type             |
      | network_zone     | System        | network_zone     |

