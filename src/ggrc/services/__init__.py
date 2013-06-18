# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

from collections import namedtuple
from .common import *

"""All gGRC REST services."""

ServiceEntry = namedtuple('ServiceEntry', 'name model_class service_class')

def service(name, model_class, service_class=Resource):
  return ServiceEntry(name, model_class, service_class)

def all_collections():
  """The list of all gGRC collection services as a list of
  (url, ModelClass) tuples.
  """
  import ggrc.models.all_models as models

  return [
    service('categorizations', models.Categorization),
    service('categories', models.Category),
    service('controls', models.Control),
    service('control_assessments', models.ControlAssessment),
    service('control_controls', models.ControlControl),
    service('control_risks', models.ControlRisk),
    service('control_sections', models.ControlSection),
    service('cycles', models.Cycle),
    service('data_assets', models.DataAsset),
    service('directives', models.Directive),
    service('documents', models.Document),
    service('facilities', models.Facility),
    service('help', models.Help),
    service('markets', models.Market),
    service('meetings', models.Meeting),
    service('object_documents', models.ObjectDocument),
    service('object_people', models.ObjectPerson),
    service('options', models.Option),
    service('org_groups', models.OrgGroup),
    service('pbc_lists', models.PbcList),
    service('people', models.Person),
    service('population_samples', models.PopulationSample),
    service('products', models.Product),
    service('projects', models.Project),
    service('programs', models.Program),
    service('program_directives', models.ProgramDirective),
    service('relationships', models.Relationship),
    service('requests', models.Request),
    service('responses', models.Response),
    service('risks', models.Risk),
    service('risky_attributes', models.RiskyAttribute),
    service('risk_risky_attributes', models.RiskRiskyAttribute),
    service('sections', models.Section),
    service('systems', models.System),
    service('systems_systems', models.SystemSystem),
    service('system_controls', models.SystemControl),
    service('transactions', models.Transaction),
    ]

def init_all_services(app):
  """Register all gGRC REST services with the Flask application ``app``."""
  #from .common import Resource
  from ggrc.login import login_required

  for entry in all_collections():
    entry.service_class.add_to(
      app,
      '/api/{0}'.format(entry.name),
      entry.model_class,
      decorators=(login_required,),
      )

  from .search import search
  app.add_url_rule(
    '/search', 'search', login_required(search))

  from .log_event import log_event
  app.add_url_rule(
    '/api/log_events', 'log_events', log_event, methods=['POST'])

  from .description import ServiceDescription
  app.add_url_rule(
    '/api', view_func=ServiceDescription.as_view('ServiceDescription'))
