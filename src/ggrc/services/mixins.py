#Identifiable, ChangeTracked are left out on purpose - clients don't get to
#redefine these attributes. In fact - it may be that an error should be raised
#if the submitted content tries to...

class Described(object):
  def update_object(self, tgt, src):
    tgt.description = src.get('description')

class Hyperlinked(object):
  def update_object(self, tgt, src):
    tgt.url = src.get('url')

#TODO class Hierarchical(object):

class Timeboxed(object):
  def update_object(self, tgt, src):
    tgt.start_date = src.get('start_date')
    tgt.end_date = src.get('end_date')

class Slugged(object):
  def update_object(self, tgt, src):
    tgt.slug = src.get('slug')
    tgt.title = src.get('title')
