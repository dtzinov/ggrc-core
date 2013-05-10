from .all_models import *

"""All gGRC model objects and associated utilities."""

def create_db():
  # FIXME: Should not have to import app
  from ggrc import db, app
  import ggrc.models.all_models
  print("Creating database")
  db.create_all()

