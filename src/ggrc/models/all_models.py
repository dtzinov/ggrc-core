
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

"""All gGRC model classes grouped together for convenience."""

# TODO: Implement with Authentication
#from .account import Account
from .categorization import Categorization
from .category import Category
from .control import Control
from .control_assessment import ControlAssessment
from .control_control import ControlControl
from .control_risk import ControlRisk
from .control_section import ControlSection
from .cycle import Cycle
from .data_asset import DataAsset
from .directive import Directive
from .document import Document
from .facility import Facility
from .help import Help
from .market import Market
from .meeting import Meeting
from .object_document import ObjectDocument
from .object_person import ObjectPerson
from .option import Option
from .org_group import OrgGroup
from .pbc_list import PbcList
from .person import Person
from .population_sample import PopulationSample
from .product import Product
from .program import Program
from .program_directive import ProgramDirective
from .project import Project
from .relationship import Relationship, RelationshipType

#TODO: This isn't currently used
#from .relationship_type import RelationshipType
from .request import Request
from .response import Response
from .risk import Risk
from .risk_risky_attribute import RiskRiskyAttribute
from .risky_attribute import RiskyAttribute
from .section import Section
from .system import System
from .system_control import SystemControl

# TODO: Is this used?
#from .system_section import SystemSection
from .system_system import SystemSystem
from .transaction import Transaction

# TODO: Include?
from .version import Version
from .log_event import LogEvent

all_models = [
  Categorization,
  Category,
  Control,
  ControlAssessment,
  ControlControl,
  ControlRisk,
  ControlSection,
  Cycle,
  DataAsset,
  Directive,
  Document,
  Facility,
  Help,
  Market,
  Meeting,
  ObjectDocument,
  ObjectPerson,
  Option,
  OrgGroup,
  PbcList,
  Person,
  PopulationSample,
  Product,
  Program,
  ProgramDirective,
  Project,
  Relationship,
  RelationshipType,
  Request,
  Response,
  Risk,
  RiskRiskyAttribute,
  RiskyAttribute,
  Section,
  System,
  SystemControl,
  SystemSystem,
  Transaction,
  Version,
  LogEvent,
  ]

__all__ = [model.__name__ for model in all_models]
