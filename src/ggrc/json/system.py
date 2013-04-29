from .common import Builder

class System(Builder):
  _publish_attrs = [
      'infrastructure',
      #'owner_id, this should probably be a "Person"
      'is_biz_process',
      #'type_id', this should be a Type
      'version',
      'notes',
      #'network_zone_id',
      ]
