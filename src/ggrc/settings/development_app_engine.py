# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

DEBUG = True
TESTING = True
HOST = '0.0.0.0'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:root@localhost/ggrcdev'
FULLTEXT_INDEXER = 'ggrc.fulltext.mysql.MysqlIndexer'
LOGIN_MANAGER = 'ggrc.login.appengine'
#SQLALCHEMY_ECHO = True
AUTOBUILD_ASSETS = False
ENABLE_JASMINE = False

APP_ENGINE = True
