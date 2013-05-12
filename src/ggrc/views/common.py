from ggrc.services.common import ModelView
from flask import request, render_template, current_app


class BaseObjectView(ModelView):
  template = 'base_objects/show.haml'

  def dispatch_request(self, *args, **kwargs):
    method = request.method.lower()

    if method == 'get':
      if self.pk in kwargs and kwargs[self.pk] is not None:
        return self.get(*args, **kwargs)
      else:
        # No `pk` given; fallthrough for now
        pass
    else:
      # Method not supported; fallthrough for now
      pass

    raise NotImplementedError()

  def get_context_for_object(self, obj):
    return {
      'instance': obj,
      'controller': self
      }

  def render_template_for_object(self, obj):
    context = self.get_context_for_object(obj)
    return render_template(self.template, **context)

  def get(self, id):
    obj = self.get_object(id)
    if obj is None:
      return self.not_found_response()
    if 'Accept' in self.request.headers and \
       'text/html' not in self.request.headers['Accept']:
      return current_app.make_response((
        'text/html', 406, [('Content-Type', 'text/plain')]))

    rendered_template = self.render_template_for_object(obj)

    # FIXME: Etag based on rendered output, or object itself?
    #if 'If-None-Match' in self.request.headers and \
    #    self.request.headers['If-None-Match'] == self.etag(object_for_json):
    #  return current_app.make_response((
    #    '', 304, [('Etag', self.etag(object_for_json))]))

    return rendered_template

  @classmethod
  def add_to(cls, app, url, model_class=None):
    if model_class:
      view_class = type('%sObjectView' % (model_class.__name__), (BaseObjectView,), {
        '_model': model_class
        })
      import ggrc.views
      setattr(ggrc.views, model_class.__name__, view_class)
    else:
      view_class = cls

    view_func = view_class.as_view(view_class.endpoint_name())
    view_route = '%s/<%s:%s>' % (url, cls.pk_type, cls.pk)
    app.add_url_rule(view_route,
      view_func=view_func,
      methods=['GET'])
