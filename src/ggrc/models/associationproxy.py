from sqlalchemy.ext.associationproxy \
    import association_proxy as orig_association_proxy

def resolve_class(model_class):
  if type(model_class) is str:
    import ggrc.models
    return getattr(ggrc.models, model_class)
  return model_class

def association_proxy(target_collection, attr, model_class):
  #FIXME is model_class needed? can't that be determined off of reflection?!
  return orig_association_proxy(target_collection, attr, creator=\
      lambda arg: resolve_class(model_class)(**{
        attr: arg,
        'modified_by_id': 1, #FIXME
        }))

