from ggrc import models
from .common import Resource

class Categorization(Resource):
  _model = models.Category

  def update_object(self, categorization, src):
    pass

  def attrs_for_json(self, object):
    pass

