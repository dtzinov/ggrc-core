# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

import datetime
import iso8601
from sqlalchemy import and_, cast
from sqlalchemy.types import AbstractType, Boolean, Date, DateTime
from werkzeug.exceptions import BadRequest

class AttributeQueryBuilder(object):
  def __init__(self, model):
    self.model = model

  def bad_query_parameter(self, attrname):
    return BadRequest(
        'Unknown or unsupported query parameter {0}'.format(attrname))

  def get_attr_for_model(self, attrname, model):
    #FIXME Differentiating bad parameter to allow it through, for now
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

  def process_property_path(self, arg, value, joinlist, filters):
    segments = arg.split('.')
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
      attr = self.get_attr_for_model(arg, self.model)
      self.check_valid_property(attr, arg)
    value = self.coerce_value_for_query_param(attr, arg, value)
    filters.append(attr == cast(value, attr.type))

  def collection_filters(self, args):
    """Create filter expressions using ``request.args``"""
    joinlist = []
    filter_expressions = []
    for arg, value in args.items():
      self.process_property_path(arg, value, joinlist, filter_expressions)
    filter = filter_expressions[0]
    for f in filter_expressions[1:]:
      filter = and_(f)
    return (filter, joinlist)

