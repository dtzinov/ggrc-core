from .common import build

class Categorization(object):
  @classmethod
  def build_contribution(cls, obj):
    return {
        'category': build(obj.category),
        'categorizable': build(obj.categorizable),
        }
