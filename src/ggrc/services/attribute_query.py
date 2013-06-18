# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

import datetime
import iso8601
from collections import namedtuple
from sqlalchemy import and_, cast
from sqlalchemy.types import AbstractType, Boolean, Date, DateTime
from werkzeug.exceptions import BadRequest

AttributeQuery = namedtuple('AttributeQuery', 'filter joinlist')

class AttributeQueryBuilder(object):
  def __init__(self, model):
    self.model = model

  def bad_query_parameter(self, attrname):
    return BadRequest(
        'Unknown or unsupported query parameter {0}'.format(attrname))

  def get_attr_for_model(self, attrname, model):
    if not hasattr(model, attrname):
      raise self.bad_query_parameter(attrname)
    attr = getattr(model, attrname)
    return attr

  def coerce_value_for_query_param(self, attr, arg, value):
    attr_type = type(attr.type)
    if attr_type is Boolean:
      value = value.lower()
      if value == 'true':
        value = True
      elif value == 'false':
        value = False
      else:
        raise BadRequest('{0} must be "true" or "false", not {1}.'.format(
          arg, value))
    elif attr_type is DateTime:
      try:
       value = iso8601.parse_date(value)
      except iso8601.ParseError as e:
        raise BadRequest(
            'Malformed DateTime {0} for parameter {0}. '
            'Error message was: {1}'.format(value, arg, e.message)
            )
    elif attr_type is Date:
      try:
        value = datetime.datetime.strptime(value, '%Y-%m-%d')
      except ValueError as e:
        raise BadRequest(
            'Malformed Date {0} for parameter {1}. '
            'Error message was: {2}'.format(value, arg, e.message)
            )
    return value

  def check_valid_property(self, attr, attrname):
    if not hasattr(attr, 'type') or \
        not isinstance(attr.type, AbstractType):
      raise self.bad_query_parameter(attrname)

  def process_property_path(self, arg, value):
    joinlist = []
    filters = []
    clean_arg = arg if not arg.endswith('__in') else arg[0:-4]
    segments = clean_arg.split('.')
    if len(segments) > 1:
      current_model = self.model
      attr = None
      for segment in segments:
        if attr:
          current_model = attr.mapper.class_
          joinlist.append(attr)
        attr = self.get_attr_for_model(segment, current_model)
      self.check_valid_property(attr, segment)
    else:
      attr = self.get_attr_for_model(clean_arg, self.model)
      self.check_valid_property(attr, clean_arg)
    if arg.endswith('__in'):
      value = value.split(',')
      value = [self.coerce_value_for_query_param(attr, arg, v) for v in value]
      filters.append(attr.in_(value))
    else:
      value = self.coerce_value_for_query_param(attr, arg, value)
      filters.append(attr == cast(value, attr.type))
    return joinlist, filters

  def collection_filters(self, args):
    """Create filter expressions using ``request.args``"""
    filter = None
    joinlist = []
    filter_expressions = []
    for arg, value in args.items():
      try:
        joins, filters = self.process_property_path(arg, value)
        joinlist.extend(joins)
        filter_expressions.extend(filters)
      except BadRequest:
        # FIXME: raise BadRequest when client-side is ready for it
        # * when fixed, remove appropriate @wip's in 
        #   service_specs/query.feature
        pass
    if filter_expressions:
      filter = filter_expressions[0]
      for f in filter_expressions[1:]:
        filter = and_(filter, f)
    return AttributeQuery(filter, joinlist)
