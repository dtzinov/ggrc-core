
from ggrc.app import app
import ggrc.views
"""Filters for GRC specific Jinja processing
"""

@app.template_filter("viewlink")
def view_link_filter(obj):
  """Create a view link for an object, that navigates
  to its object-view page in the app
  """
  view = getattr(ggrc.views, obj.__class__.__name__, None)
  return view.url_for(obj) if view else None

# Additional template filters
#

@app.template_filter("underscore")
def underscore_filter(s):
  """Change spaces to underscores and make lowercase
  """
  return "_".join(s.lower().split(' '))

@app.template_filter("nospace")
def nospace_filter(s):
  """Remove spaces
  """
  return "".join(s.split(' '))
