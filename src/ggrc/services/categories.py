from ggrc import models
from .common import Resource

class Category(Resource):
  _model = models.Category

  # Method overrides
  def update_object(self, category, src):
    category.name = src.get("name", "")

  def attrs_for_json(self, object):
    return { 'name': object.name, }
