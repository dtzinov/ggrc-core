import sys

def service_for(obj):
  module = sys.modules['ggrc.services']
  if type(obj) is str:
    model_type = obj
  else:
    model_type = obj.__class__.__name__
  return getattr(module, model_type, None)

def url_for(obj, id=None):
  service = service_for(obj)
  if service is None:
    return None
  if id:
    return service.url_for(id)
  return service.url_for(obj)
