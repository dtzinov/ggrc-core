from ggrc import models
from .common import Resource

class Category(Resource):
  _model = models.Category

  # Method overrides
  def update_object(self, category, src):
    category.name = src.get("name", "")

