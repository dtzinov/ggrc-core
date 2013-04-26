class Slugged(object):
  def update_object(self, control, src):
    print src
    print src.get('slug')
    control.slug = src.get('slug')
    control.title = src.get('title')
