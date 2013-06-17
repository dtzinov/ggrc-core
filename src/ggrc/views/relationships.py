"""Related objects service
"""

from ggrc.app import app
from ggrc.models.relationship import Relationship
from ggrc.models.relationship_types import RelationshipTypes
from ggrc.services.common import as_json
import ggrc.builder

from flask import url_for, request, current_app
from werkzeug.urls import url_encode

class RelatedObjectResults(object):
  def __init__(self, obj_id, obj_type, far_type):
    self.obj_id = obj_id
    self.obj_type = obj_type
    self.far_type = far_type

    self.obj_real_type = 'System' if obj_type == 'Process' else obj_type
    self.far_real_type = 'System' if far_type == 'Process' else far_type

  def related_is_src_query(self, vr):
    return Relationship.query.filter_by(
      destination_type=self.obj_real_type,
      destination_id=self.obj_id,
      source_type=self.far_real_type,
      relationship_type_id=vr['relationship_type'])

  def related_is_dst_query(self, vr):
    return Relationship.query.filter_by(
      source_type=self.obj_real_type,
      source_id=self.obj_id,
      destination_type=self.far_real_type,
      relationship_type_id=vr['relationship_type'])

  def get_edit_url(self, vr):
    return "{base_url}?{params}".format(
      base_url='/api/relationships',
      params=url_encode(dict(
        object_id=self.obj_id,
        object_type=self.obj_type,
        relationship_type=vr['relationship_type'],
        related_side=vr['related_model_endpoint'],
        related_model=self.far_type)))

  def get_valid_relationships(self):
    return [
      vr for vr in RelationshipTypes.valid_relationships(self.obj_type)
        if vr['related_model'] == self.far_type]

  def get_results(self):
    return [self.get_result(vr) for vr in self.get_valid_relationships()]

  def get_relationship_type(self, vr):
    return RelationshipTypes.get_type(vr['relationship_type'])

  def get_result_related_object(self, obj):
    data = ggrc.builder.json.publish(obj)
    return { 'url': data['viewLink'], 'object': data }

  def get_result_related_objects(self, objects):
    return [self.get_result_related_object(obj) for obj in objects]

  def get_result(self, vr):
    rt = self.get_relationship_type(vr)

    if vr['related_model_endpoint'] == 'both' and \
        self.far_type == self.obj_type and rt['symmetric']:
      direction = 'forward'
      objects = \
        [o.source for o in self.related_is_src_query(vr).all()] + \
        [o.destination for o in self.related_is_dst_query(vr).all()]
    else:
      if vr['related_model_endpoint'] in ('both', 'source'):
        direction = 'reverse'
        objects = [o.source for o in self.related_is_src_query(vr).all()]
      if vr['related_model_endpoint'] in ('both', 'destination'):
        direction = 'forward'
        objects = [o.destination for o in self.related_is_dst_query(vr).all()]

    return {
        'relationship_type': {
          'id': vr['relationship_type'],
          'title': self.get_title(vr, direction),
          'description': self.get_description(vr, direction),
          'related_type': self.far_type, #.underscore.pluralize,
          'related_side': "source" if direction == "forward" else "destination",
          'edit_url': self.get_edit_url(vr),
          },
        'related_objects': self.get_result_related_objects(objects)
      }

  def get_description(self, vr, direction='forward'):
    rt = self.get_relationship_type(vr)
    if rt:
      return rt['{0}_description'.format(direction)]
    else:
      return "Unknown relationship type"

  def get_title(self, vr, direction='forward'):
    rt = self.get_relationship_type(vr)
    if rt:
      return "{obj_type} {phrase} {far_type}".format(
        obj_type=self.obj_type, #.titleize,
        phrase=rt['{0}_phrase'.format(direction)],
        far_type=self.far_type) #.pluralize) #.titleize)
    else:
      return "{relationship_type}:source".format(
        relationship_type=vr['relationship_type'])


@app.route('/relationships/related_objects')
def related_objects():
  obj_id = request.args['oid']
  obj_type = request.args['otype']
  far_type = request.args['related_model']

  related_object_results = RelatedObjectResults(obj_id, obj_type, far_type)
  results = related_object_results.get_results()

  current_app.make_response((
      'application/json', 200, [('Content-Type', 'application/json')]))
  return as_json(results)

def related_objects_link(obj_id, obj_type, far_type):
  return "{base_url}?{params}".format(
      base_url=url_for('related_objects'),
      params=url_encode(dict(
        oid=obj_id, otype=obj_type, related_model=far_type)))

@app.context_processor
def related_objects_context():
  return dict(
      related_objects=RelationshipTypes.valid_relationships,
      related_objects_link=related_objects_link
      )
