Feature: Basic RESTful CRUD Support

  Scenario Outline: HTTP POST and GET
    Given an example "<resource_type>"
    When the example "<resource_type>" is POSTed to the "<collection>"
    Then a 201 status code is received
    And the response has a Location header
    And we receive a valid "<resource_type>" in the entity body
    And the received "<resource_type>" matches the one we posted

  Examples: Resources
      | resource_type      | collection                 |
      #| Categorization     | /api/categorizations       |
      #| Category           | /api/categories            |
      | Control            | /api/controls              |
      #| ControlAssessment  | /api/control_assessments   |
      #| ControlRisk        | /api/control_risks         |
      #| Cycle              | /api/cycles                |
      #| DataAsset          | /api/data_assets           |
      #| Directive          | /api/directives            |
      #| Document           | /api/documents             |
      #| Facility           | /api/facilities            |
      #| Market             | /api/markets               |
      #| Meeting            | /api/meetings              |
      #| ObjectDocument     | /api/object_documents      |
      #| ObjectPerson       | /api/object_people         |
      #| Option             | /api/options               |
      #| OrgGroup           | /api/org_groups            |
      #| PbcList            | /api/pbc_lists             |
      #| Person             | /api/people                |
      #| PopulationSample   | /api/population_samples    |
      #| Product            | /api/products              |
      #| Project            | /api/projects              |
      | Program            | /api/programs              |
      #| ProgramDirective   | /api/program_directives    |
      #| Relationship       | /api/relationships         |
      #| Request            | /api/requests              |
      #| Response           | /api/responses             |
      #| Risk               | /api/risks                 |
      #| RiskyAttribute     | /api/risky_attributes      |
      #| RiskRiskyAttribute | /api/risk_risky_attributes |
      #| Section            | /api/sections              |
      #| System             | /api/systems               |
      #| SystemSystem       | /api/systems_systems       |
      #| SystemControl      | /api/system_controls       |
      #| Transaction        | /api/transactions          |

