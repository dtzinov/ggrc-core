from ggrc import models
from .common import Resource
from .mixins import Slugged

class Control(Slugged, Resource):
  _model = models.Control

  def update_object(self, control, src):
    control.version = self.getval(src, 'version', 'None')
    control.documentation_description = src.get(
        'documentation_description', None)
    control.fraud_related = src.get('fraud_related', None)
    control.key_control = src.get('key_control', None)
    control.active = src.get('active', None)
    control.notes = src.get('notes', None)
