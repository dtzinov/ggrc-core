import ggrc.json
import ggrc.services

def url_for(obj):
  service = getattr(ggrc.services, obj.__class__.__name__)
  return service.url_for(obj)

def build(obj):
  ret = {
      'id': obj.id,
      'selfLink': url_for(obj),
      'created_at': obj.created_at,
      'updated_at': obj.updated_at,
      }
  builder = getattr(ggrc.json, obj.__class__.__name__)
  ret.update(builder.build_contribution(obj))
  return ret

