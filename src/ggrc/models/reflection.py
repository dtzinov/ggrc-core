class AttributeInfo(object):
  '''Gather model CRUD information by reflecting on model classes. Builds and
  caches a list of the publishing properties for a class by walking the
  class inheritance tree.
  '''
  def __init__(self, tgt_class):
    self._publish_attrs = AttributeInfo.gather_publish_attrs(tgt_class)
    self._update_attrs = AttributeInfo.gather_update_attrs(tgt_class)
    self._create_attrs = AttributeInfo.gather_create_attrs(tgt_class)

  @classmethod
  def gather_attrs(cls, tgt_class, src_attrs, accumulator=None):
    src_attrs = src_attrs if type(src_attrs) is list else [src_attrs]
    accumulator = accumulator if accumulator is not None else set()
    for attr in src_attrs:
      attrs = tgt_class.__dict__.get(attr, None)
      if attrs is not None:
        accumulator.update(attrs)
        break
    for base in tgt_class.__bases__:
      cls.gather_attrs(base, src_attrs, accumulator)
    return accumulator

  @classmethod
  def gather_publish_attrs(cls, tgt_class):
    return cls.gather_attrs(tgt_class, '_publish_attrs')

  @classmethod
  def gather_update_attrs(cls, tgt_class):
    attrs = cls.gather_attrs(tgt_class, ['_update_attrs', '_publish_attrs'])
    return attrs

  @classmethod
  def gather_create_attrs(cls, tgt_class):
    return cls.gather_attrs(tgt_class, [
      '_create_attrs', '_update_attrs', '_publish_attrs'])
