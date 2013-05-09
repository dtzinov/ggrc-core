from .common import *

def all_collections():
  from ggrc.models import all_models as models

  return [
    ('categorizations', models.Categorization),
    ('categories', models.Category),
    ('controls', models.Control),
    ('control_assessments', models.ControlAssessment),
    ('control_risks', models.ControlRisk),
    ('cycles', models.Cycle),
    ('data_assets', models.DataAsset),
    ('directives', models.Directive),
    ('documents', models.Document),
    ('facilities', models.Facility),
    ('markets', models.Market),
    ('meetings', models.Meeting),
    ('object_documents', models.ObjectDocument),
    ('object_people', models.ObjectPerson),
    ('options', models.Option),
    ('org_groups', models.OrgGroup),
    ('pbc_lists', models.PbcList),
    ('people', models.Person),
    ('population_samples', models.PopulationSample),
    ('products', models.Product),
    ('projects', models.Project),
    ('programs', models.Program),
    ('program_directives', models.ProgramDirective),
    ('relationships', models.Relationship),
    ('requests', models.Request),
    ('responses', models.Response),
    ('risks', models.Risk),
    ('risky_attributes', models.RiskyAttribute),
    ('risk_risky_attributes', models.RiskRiskyAttribute),
    ('sections', models.Section),
    ('systems', models.System),
    ('systems_systems', models.SystemSystem),
    ('system_controls', models.SystemControl),
    ('transactions', models.Transaction),
    ]

def init_all_services(app):
  from .common import Resource

  for k,v in all_collections():
    Resource.add_to(app, '/api/{}'.format(k), v)

  from .description import ServiceDescription

  app.add_url_rule(
    '/api', view_func=ServiceDescription.as_view('ServiceDescription'))
