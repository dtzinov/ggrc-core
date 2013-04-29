from .common import Builder

class Identifiable(Builder):
  _publish_attrs = ['id']
  _update_attrs = []

class ChangeTracked(Builder):
  _publish_attrs = [
      #'modified_by_id' link to person??
      'created_at',
      'updated_at',
      ]
  _update_attrs = []

class Described(Builder):
  _publish_attrs = ['description']

class Hyperlinked(Builder):
  _publish_attrs = ['url']

#TODO class Hierarchical(Builder):
#requires the related to be scoped... should produce _only_ the hyperlinks for
#parent and children, probably...

class Timeboxed(Builder):
  _publish_attrs = ['start_date', 'end_date']

class Slugged(Builder):
  _publish_attrs = ['slug', 'title']
  _update_attrs = ['slug', 'title'] #FIXME Should slug be modifiable??
  _create_attrs = _publish_attrs

# BusinessObject has no properties of its own; it's intentionally left out.
