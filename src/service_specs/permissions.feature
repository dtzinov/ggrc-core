Feature: RBAC Permissions enforcement for REST API

  Background:
    Given service description

  Scenario Outline: POST requires create permission for the context
    Given current user is "{\"email\": \"tester@testertester.com\", \"name\": \"Jo Tester\", \"permissions\": {\"create\": {\"<resource_type>\": [1111]}}}"
    And a new "<resource_type>" named "resource"
    And "resource" property "context_id" is literal "1111"
    Then POST of "resource" to its collection is allowed
    Given a new "<resource_type>" named "resource"
    And "resource" property "context_id" is literal "1112"
    Then POST of "resource" to its collection is forbidden

  Examples:
      | resource_type      |
      | Category           |
      | Control            |
      | ControlAssessment  |
      | ControlRisk        |
      | Cycle              |
      | DataAsset          |
      | Directive          |
      | Document           |
      | Facility           |
      | Help               |
      | Market             |
      | Meeting            |
      | Option             |
      | OrgGroup           |
      | PbcList            |
      | Person             |
      | PopulationSample   |
      | Product            |
      | Project            |
      | Program            |
      | ProgramDirective   |
      | Request            |
      | Response           |
      | Risk               |
      | RiskyAttribute     |
      | RiskRiskyAttribute |
      | Section            |
      | System             |
      | SystemSystem       |
      | SystemControl      |
      | Transaction        |

  Scenario Outline: GET requires read permission for the context
    Given current user is "{\"email\": \"tester@testertester.com\", \"name\": \"Jo Tester\", \"permissions\": {\"create\": {\"<resource_type>\": [1111]}, \"read\": {\"<resource_type>\": [1111]}}}"
    And a new "<resource_type>" named "resource"
    And "resource" property "context_id" is literal "1111"
    And "resource" is POSTed to its collection
    Then GET of "resource" is allowed
    Given current user is "{\"email\": \"bobtester@testertester.com\", \"name\": \"Bob Tester\", \"permissions\": {\"create\": {\"<resource_type>\": [1112]}}}"
    Then GET of "resource" is forbidden

  Examples:
      | resource_type      |
      | Category           |
      | Control            |
      | ControlAssessment  |
      | ControlRisk        |
      | Cycle              |
      | DataAsset          |
      | Directive          |
      | Document           |
      | Facility           |
      | Help               |
      | Market             |
      | Meeting            |
      | Option             |
      | OrgGroup           |
      | PbcList            |
      | Person             |
      | PopulationSample   |
      | Product            |
      | Project            |
      | Program            |
      | ProgramDirective   |
      | Request            |
      | Response           |
      | Risk               |
      | RiskyAttribute     |
      | RiskRiskyAttribute |
      | Section            |
      | System             |
      | SystemSystem       |
      | SystemControl      |
      | Transaction        |

  Scenario Outline: PUT requires update permission for the context
    Given current user is "{\"email\": \"tester@testertester.com\", \"name\": \"Jo Tester\", \"permissions\": {\"create\": {\"<resource_type>\": [1111]}, \"read\": {\"<resource_type>\": [1111]}, \"update\": {\"<resource_type>\": [1111]}}}"
    And a new "<resource_type>" named "resource"
    And "resource" property "context_id" is literal "1111"
    And "resource" is POSTed to its collection
    Then GET of "resource" is allowed
    Then PUT of "resource" is allowed
    Given current user is "{\"email\": \"bobtester@testertester.com\", \"name\": \"Bob Tester\", \"permissions\": {\"create\": {\"<resource_type>\": [1112]}, \"read\": {\"<resource_type>\": [1111]}}}"
    Then GET of "resource" is allowed
    Then PUT of "resource" is forbidden

  Examples:
      | resource_type      |
      | Category           |
      | Control            |
      | ControlAssessment  |
      | ControlRisk        |
      | Cycle              |
      | DataAsset          |
      | Directive          |
      | Document           |
      | Facility           |
      | Help               |
      | Market             |
      | Meeting            |
      | Option             |
      | OrgGroup           |
      | PbcList            |
      | Person             |
      | PopulationSample   |
      | Product            |
      | Project            |
      | Program            |
      | ProgramDirective   |
      | Request            |
      | Response           |
      | Risk               |
      | RiskyAttribute     |
      | RiskRiskyAttribute |
      | Section            |
      | System             |
      | SystemSystem       |
      | SystemControl      |
      | Transaction        |

  @wip
  Scenario Outline: DELETE requires delete permission for the context
    Given current user is "{\"email\": \"tester@testertester.com\", \"name\": \"Jo Tester\", \"permissions\": {\"create\": {\"<resource_type>\": [1111]}, \"read\": {\"<resource_type>\": [1111]}, \"update\": {\"<resource_type>\": [1111]}}}"
    And a new "<resource_type>" named "resource"
    And "resource" property "context_id" is literal "1111"
    And "resource" is POSTed to its collection
    Then GET of "resource" is allowed
    Then DELETE of "resource" is forbidden 
    Given current user is "{\"email\": \"bobtester@testertester.com\", \"name\": \"Bob Tester\", \"permissions\": {\"create\": {\"<resource_type>\": [1112]}, \"read\": {\"<resource_type>\": [1111]}, \"delete\": {\"<resource_type>\": [1111]}}}"
    Then GET of "resource" is allowed
    Then DELETE of "resource" is allowed

  Examples:
      | resource_type      |
      | Category           |

