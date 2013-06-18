# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

DEBUG = False
TESTING = False

# Flask-SQLAlchemy fix to be less than `wait_time` in /etc/mysql/my.cnf
SQLALCHEMY_POOL_RECYCLE = 120

# Settings in app.py
AUTOBUILD_ASSETS = False
ENABLE_JASMINE = False
FULLTEXT_INDEXER = None
USER_PERMISSIONS_PROVIDER = None

# Deployment-specific variables
COMPANY = "Company, Inc."
COMPANY_LOGO_TEXT = "Company GRC"
VERSION = "s5"

# Initialize from environment if present
import os
SQLALCHEMY_DATABASE_URI = os.environ.get('GGRC_DATABASE_URI', '')
SECRET_KEY = os.environ.get('GGRC_SECRET_KEY', 'Replace-with-something-secret')
