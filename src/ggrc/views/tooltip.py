# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from .common import BaseObjectView

class TooltipView(BaseObjectView):
  model_template = '{model_plural}/tooltip.haml'
  base_template = 'base_objects/tooltip.haml'

  @classmethod
  def add_to(cls, app, url, model_class=None, decorators=()):
    if model_class:
      view_class_name = '{0}TooltipView'.format(model_class.__name__)
      view_class = type(
          view_class_name,
          (TooltipView,),
          {'_model': model_class},
          )
      import ggrc.views
      setattr(ggrc.views, view_class_name, view_class)
    else:
      view_class = cls
    view_func = view_class.as_view(view_class.endpoint_name())
    view_func = cls.decorate_view_func(view_func, decorators)
    view_route = '{url_prefix}/<{pk_type}:{pk}>/tooltip'.format(
        url_prefix=url,
        pk_type=cls.pk_type,
        pk=cls.pk,
        )
    app.add_url_rule(view_route,
        view_func=view_func,
        methods=['GET'],
        )
