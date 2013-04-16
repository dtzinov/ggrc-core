from flask import current_app
from ggrc import db, models
from .common import Resource

class Category(Resource):
  _model = models.Category

  def get(self, id):
    category = self.get_object(id)

    if category is None:
      return current_app.make_response(('Category not found.', 404,[]))

    return self.json_success_response(
      self.object_for_json(category))

  def put(self, id):
    category = self.get_object(id)

    if category is None:
      return current_app.make_response(('Category not found.', 404,[]))
    else:
      self.update_object_from_form(category, self.request.form)
      db.session.add(category)
      db.session.commit()

      return self.json_success_response(
        self.object_as_json(category))

  def delete(self, id):
    category = self.get_object(id)

    if category is None:
      return current_app.make_response(('Category not found.', 404,[]))
    else:
      db.session.delete(category)
      return self.json_success_response(
        self.object_as_json(category))

  def collection_get(self):
    categories = self.get_collection()

    return self.json_success_response(
      self.collection_for_json(categories))

  def collection_post(self):
    category = self.model()

    self.update_object_from_form(category, self.request.form)

    category.name = self.request.form.get("name", "")
    db.session.add(category)
    db.session.commit()

    return self.json_success_response(
      self.object_for_json(category))

  # Model/DB helpers
  def update_object_from_form(self, category, form):
    category.name = form.get("name", "")

  def get_collection(self):
    return db.session.query(self.model)

  def get_object(self, id):
    # This could also use `self.pk`
    return self.get_collection().filter(self.model.id == id).first()

  # Response helpers
  def json_success_response(self, response_object):
    return current_app.make_response(
      (self.as_json(response_object), 200, []))

  def collection_for_json(self, objects):
    objects_json = []
    for object in objects:
      objects_json.append(self.object_for_json(object))

    collection_json = {
      'categories_collection': {
        'selfLink': self.url_for(),
        'categories': objects_json,
        }
      }

    return collection_json

  def object_for_json(self, object):
    return {
      'category': {
        'id': object.id,
        'selfLink': self.url_for(id=object.id),
        'name': object.name,
        'created_at': object.created_at,
        'updated_at': object.updated_at,
        }
      }

