# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from ggrc.services.common import ModelView, as_json
import ggrc.builder
from flask import request, render_template, current_app


class BaseObjectView(ModelView):
  model_template = '{model_plural}/show.haml'
  base_template = 'base_objects/show.haml'

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
      'controller': self,
      'instance_json':
        lambda: as_json({
            self.model._inflector.table_singular: ggrc.builder.json.publish(obj)
          })
      }

  def render_template_for_object(self, obj):
    context = self.get_context_for_object(obj)
    template_paths = [
      self.model_template.format(model_plural=self.model._inflector.table_plural),
      self.base_template
      ]
    return render_template(template_paths, **context)

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
  def add_to(cls, app, url, model_class=None, decorators=()):
    if model_class:
      view_class = type(
        '{0}ObjectView'.format(model_class.__name__),
        (BaseObjectView,),
        {
          '_model': model_class
        })
      import ggrc.views
      setattr(ggrc.views, model_class.__name__, view_class)
    else:
      view_class = cls

    view_func = view_class.as_view(view_class.endpoint_name())
    view_func = cls.decorate_view_func(view_func, decorators)
    view_route = '{url}/<{type}:{pk}>'.format(
        url=url, type=cls.pk_type, pk=cls.pk)
    app.add_url_rule(view_route,
      view_func=view_func,
      methods=['GET'])
