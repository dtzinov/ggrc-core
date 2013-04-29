from .common import publish

class Categorization(object):
  @classmethod
  def publish_attrs(cls, obj, json_obj):
    json_obj['category'] = publish(obj.category)
    json_obj['categorizable'] = publish(obj.categorizable)
