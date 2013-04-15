from flask.views import MethodView
from flask import url_for

class Resource(MethodView):
  @classmethod
  def endpoint_name(cls):
    return cls.__name__

  def url_for(self, *args, **kwargs):
    return url_for(self.endpoint_name(), *args, **kwargs)

  @classmethod
  def add_to(cls, app, url_pattern):
    app.add_url_rule(url_pattern, view_func=cls.as_view(cls.endpoint_name()))


