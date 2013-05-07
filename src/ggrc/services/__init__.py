from .common import *

def init_all_services(app):
  from ggrc.models import *
  from .common import Resource

  for k,v in [
      ('categorizations', Categorization),
      ('categories', Category),
      ('controls', Control),
      ('control_assessments', ControlAssessment),
      ('control_risks', ControlRisk),
      ('cycles', Cycle),
      ('data_assets', DataAsset),
      ('directives', Directive),
      ('documents', Document),
      ('facilities', Facility),
      ('markets', Market),
      ('meetings', Meeting),
      ('object_documents', ObjectDocument),
      ('object_people', ObjectPerson),
      ('options', Option),
      ('org_groups', OrgGroup),
      ('pbc_lists', PbcList),
      ('people', Person),
      ('population_samples', PopulationSample),
      ('products', Product),
      ('projects', Project),
      ('programs', Program),
      ('program_directives', ProgramDirective),
      ('relationships', Relationship),
      ('requests', Request),
      ('responses', Response),
      ('risks', Risk),
      ('risky_attributes', RiskyAttribute),
      ('risk_risky_attributes', RiskRiskyAttribute),
      ('sections', Section),
      ('systems', System),
      ('systems_systems', SystemSystem),
      ('system_controls', SystemControl),
      ('transactions', Transaction),
      ]:
    Resource.add_to(app, '/api/{}'.format(k), v)
