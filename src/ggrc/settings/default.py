DEBUG = False
TESTING = False
AUTOBUILD_ASSETS = False
ENABLE_JASMINE = False

# Deployment-specific variables
COMPANY = "Company, Inc."
VERSION = "s3"

# Initialize from environment if present
import os
SQLALCHEMY_DATABASE_URI = os.environ.get('GGRC_DATABASE_URI', '')
