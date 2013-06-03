
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from .all_models import *

"""All gGRC model objects and associated utilities."""

def create_db_with_create_all():
  from ggrc.app import db
  import ggrc.models.all_models
  db.create_all()

def create_db_with_migrations(quiet=False):
  from ggrc.app import db
  from alembic.config import main
  import logging
  if quiet:
    logging.disable(logging.INFO)
  main(["-c", "migrations/alembic.ini", "upgrade", "head"])
  if quiet:
    logging.disable(logging.NOTSET)

def drop_db_with_drop_all():
  from ggrc.app import db
  import ggrc.models.all_models
  db.drop_all()

def drop_db_with_migrations(quiet=False):
  from ggrc.app import db
  from alembic.config import main
  import logging
  if quiet:
    logging.disable(logging.INFO)
  main(["-c", "migrations/alembic.ini", "downgrade", "base"])
  if quiet:
    logging.disable(logging.NOTSET)
  # Finally, clean up alembic_version itself
  db.session.execute('DROP TABLE alembic_version')

def create_db(use_migrations=False, quiet=False):
  if use_migrations:
    create_db_with_migrations(quiet)
  else:
    create_db_with_create_all()

def drop_db(use_migrations=False, quiet=False):
  if use_migrations:
    drop_db_with_migrations(quiet)
  else:
    drop_db_with_drop_all()