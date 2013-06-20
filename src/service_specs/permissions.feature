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
  Scenario: Property link objects can be included with __include if the user has read access to the target
    Given current user is "{\"email\": \"bobtester@testertester.com\", \"name\": \"Bob Tester\", \"permissions\": {\"create\": {\"Directive\": [1,2], \"Program\": [1,2]}, \"read\": {\"Directive\": [1,2], \"Program\": [1,2]}, \"update\": {\"Directive\": [1,2]}}}"
    And a new "Directive" named "directive_in_1"
    And "directive_in_1" property "kind" is "Testing__include1"
    And "directive_in_1" property "context_id" is literal "1"
    And "directive_in_1" is POSTed to its collection
    And a new "Directive" named "directive_in_2"
    And "directive_in_2" property "kind" is "Testing__include1"
    And "directive_in_2" property "context_id" is literal "2"
    And "directive_in_2" is POSTed to its collection
    And a new "Program" named "program"
    And "directive_in_1" is added to links property "directives" of "program"
    And "directive_in_2" is added to links property "directives" of "program"
    And "program" property "context_id" is literal "1"
    And "program" is POSTed to its collection
    When Querying "Program" with "program_directives.directive.kind=Testing__include1&__include=directives"
    Then query result selfLink query string is "program_directives.directive.kind=Testing__include1&__include=directives"
    And "program" is in query result
    And evaluate "len(context.queryresultcollection['programs_collection']['programs'][0]['directives']) == 2"
    And evaluate "'kind' in context.queryresultcollection['programs_collection']['programs'][0]['directives'][0] and 'kind' in context.queryresultcollection['programs_collection']['programs'][0]['directives'][1]"
    Given current user is "{\"email\": \"tester@testertester.com\", \"name\": \"Jo Tester\", \"permissions\": {\"create\": {\"Directive\": [1]}, \"read\": {\"Directive\": [1], \"Program\": [1]}, \"update\": {\"Directive\": [1]}}}"
    When Querying "Program" with "program_directives.directive.kind=Testing__include1&__include=directives"
    Then query result selfLink query string is "program_directives.directive.kind=Testing__include1&__include=directives"
    And "program" is in query result
    And evaluate "len(context.queryresultcollection['programs_collection']['programs'][0]['directives']) == 2"
    And evaluate "'kind' in context.queryresultcollection['programs_collection']['programs'][0]['directives'][0] != 'kind' in context.queryresultcollection['programs_collection']['programs'][0]['directives'][1]"

