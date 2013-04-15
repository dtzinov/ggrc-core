import json
from flask import current_app
from ggrc import db
from ggrc.models import Category as CategoryModel
from .common import Resource

class Category(Resource):
  def get(self, category_id):
    category = db.session.query(CategoryModel).filter(
        CategoryModel.id == category_id).one()
    if category is None:
      return current_app.make_response(('Category not found.', 404,[]))
    return current_app.make_response((
        json.dumps({
          'category': {
            'id': category_id,
            'selfLink': self.url_for(category_id=category_id),
            }
          }),
        200,
        []))

  def put(self, category_id):
    return

  def delete(self, category_id):
    return

class CategoriesCollection(Resource):
  def get(self):
    return json.dumps({
        'categories_collection': {
          'selfLink': self.url_for(),
          'categories': [],
          },
        })

  def post(self):
    return json.dumps({
        'category': {
          'id': 'id_here',
          'selfLink': Category.url_for(category_id='id_here'),
          }
        })
