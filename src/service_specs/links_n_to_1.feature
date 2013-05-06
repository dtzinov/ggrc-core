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

  Examples: n-ary Link Resources
    | parent_type       | parent_collection        | child_type        | child_collection         | parent_property           | children_property                |
    | PbcList           | /api/pbc_lists           | ControlAssessment | /api/control_assessments | pbc_list                  | control_assessments              |
    | Control           | /api/controls            | ControlAssessment | /api/control_assessments | control                   | control_assessments              |
    | Program           | /api/programs            | Cycle             | /api/cycles              | program                   | cycles                           |
    | Cycle             | /api/cycles              | PbcList           | /api/pbc_lists           | audit_cycle               | pbc_lists                        |
    | Response          | /api/responses           | Meeting           | /api/meetings            | response                  | meetings                         |
    | PbcList           | /api/pbc_lists           | Request           | /api/requests            | pbc_list                  | requests                         |
    | Document          | /api/documents           | PopulationSample  | /api/population_samples  | population_document       | population_worksheets_documented |
    | Document          | /api/documents           | PopulationSample  | /api/population_samples  | sample_worksheet_document | sample_worksheets_documented     |
    | Document          | /api/documents           | PopulationSample  | /api/population_samples  | sample_evidence_document  | sample_evidences_documented      |
    | ControlAssessment | /api/control_assessments | Request           | /api/requests            | control_assessment        | requests                         |
    | Request           | /api/requests            | Response          | /api/responses           | request                   | responses                        |
    | System            | /api/systems             | Response          | /api/responses           | system                    | responses                        |
    | Directive         | /api/directives          | Section           | /api/sections            | directive                 | sections                         |
    | System            | /api/systems             | Transaction       | /api/transactions        | system                    | transactions                     |

  Scenario Outline:
    Given a new "<parent_type>" named "parent"
    And "parent" is POSTed to "<parent_collection>"
    And a new "<child_type>" named "child"
    And "child" link property "<parent_property>" is "parent"
    And "child" is POSTed to "<child_collection>"
    When GET of the resource "parent"
    And GET of the resource "child"
    Then the "<parent_property>" of "child" is a link to "parent"
    And the "<child_property>" of "parent" is a link to "child"

  Examples: 1-ary Link Resources
    | parent_type | parent_collection | child_type        | child_collection         | parent_property | child_property      |
    | Response    | /api/responses    | PopulationSample  | /api/population_samples  | response        | population_sample   |
