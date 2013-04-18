from ggrc import models
from .common import Resource

class Category(Resource):
  _model = models.Category

  # Method overrides
  def update_object_from_form(self, category, form):
    category.name = form.get("name", "")

  def attrs_for_json(self, object):
    return { 'name': object.name, }
