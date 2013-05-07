Feature: Rather than have clients keep a list of the endpoint URLs for
  gGRC-Core services, a service description document will be provided that
  lists the endpoints by name.

  Scenario: GET the service description for gGRC-CORE
    Given nothing new
    When GET of "/api" as "service_description"
    Then all expected endpoints are listed and GETtable in "service_description"
      | endpoint           |
      | Categorization     |
      | Category           |
      | Control            |
      | ControlAssessment  |
      | ControlRisk        |
      | Cycle              |
      | DataAsset          |
      | Directive          |
      | Document           |
      | Facility           |
      | Market             |
      | Meeting            |
      | ObjectDocument     |
      | ObjectPerson       |
      | Option             |
      | OrgGroup           |
      | PbcList            |
      | Person             |
      | PopulationSample   |
      | Product            |
      | Project            |
      | Program            |
      | ProgramDirective   |
      | Relationship       |
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
