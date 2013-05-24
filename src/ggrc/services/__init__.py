from .common import *

"""All gGRC REST services."""

def all_collections():
  """The list of all gGRC collection services as a list of
  (url, ModelClass) tuples.
  """
  from ggrc.models import all_models as models

  return [
    ('categorizations', models.Categorization),
    ('categories', models.Category),
    ('controls', models.Control),
    ('control_assessments', models.ControlAssessment),
    ('control_controls', models.ControlControl),
    ('control_risks', models.ControlRisk),
    ('control_sections', models.ControlSection),
    ('cycles', models.Cycle),
    ('data_assets', models.DataAsset),
    ('directives', models.Directive),
    ('documents', models.Document),
    ('facilities', models.Facility),
    ('help', models.Help),
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
  """Register all gGRC REST services with the Flask application ``app``."""
  from .common import Resource

  for k,v in all_collections():
    Resource.add_to(app, '/api/{0}'.format(k), v)

  from .search import search
  app.add_url_rule(
    '/search', 'search', search)

  from .description import ServiceDescription
  app.add_url_rule(
    '/api', view_func=ServiceDescription.as_view('ServiceDescription'))

