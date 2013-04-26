class Category(object):
  @classmethod
  def build_contribution(cls, obj):
    return {'name': obj.name}
