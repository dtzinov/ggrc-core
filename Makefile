SHELL := /bin/bash

PREFIX := $(shell pwd)

DEV_PREFIX ?= $(PREFIX)

all : $(DEV_PREFIX)/opt appengine

APPENGINE_SDK_VERSION=1.7.6
APPENGINE_ZIP_NAME=google_appengine_$(APPENGINE_SDK_VERSION).zip
APPENGINE_ZIP_HREF=http://googleappengine.googlecode.com/files/$(APPENGINE_ZIP_NAME)
APPENGINE_ZIP_PATH=$(DEV_PREFIX)/opt/$(APPENGINE_ZIP_NAME)
APPENGINE_SDK_PATH=$(DEV_PREFIX)/opt/google_appengine
APPENGINE_SQLITE_PATCH_PATH=$(PREFIX)/extras/google_appengine__enable_sqlite3.diff
APPENGINE_NOAUTH_PATCH_PATH=$(PREFIX)/extras/google_appengine__force_noauth_local_webserver.diff

APPENGINE_PACKAGES_ZIP=$(PREFIX)/src/packages.zip
APPENGINE_PACKAGES_DIR=$(DEV_PREFIX)/opt/gae_packages

APPENGINE_ENV_DIR=$(DEV_PREFIX)/opt/gae_virtualenv
APPENGINE_REQUIREMENTS_TXT=$(PREFIX)/src/requirements.txt

$(APPENGINE_SDK_PATH) : $(APPENGINE_ZIP_PATH)
	@echo $( dirname $(APPENGINE_ZIP_PATH) )
	cd `dirname $(APPENGINE_SDK_PATH)`; \
		unzip $(APPENGINE_ZIP_PATH)
	touch $(APPENGINE_SDK_PATH)
	cd $(APPENGINE_SDK_PATH); \
		patch -p1 < $(APPENGINE_SQLITE_PATCH_PATH); \
		patch -p1 < $(APPENGINE_NOAUTH_PATCH_PATH)

appengine_sdk : $(APPENGINE_SDK_PATH)

clean_appengine_sdk :
	rm -rf -- "$(APPENGINE_SDK_PATH)"
	rm -f "$(APPENGINE_ZIP_PATH)"

$(DEV_PREFIX)/opt :
	mkdir $(DEV_PREFIX)/opt

$(APPENGINE_ZIP_PATH) :
	wget "$(APPENGINE_ZIP_HREF)" -O "$(APPENGINE_ZIP_PATH).tmp"
	mv "$(APPENGINE_ZIP_PATH).tmp" "$(APPENGINE_ZIP_PATH)"

clean_appengine_packages :
	rm -f -- "$(APPENGINE_PACKAGES_ZIP)"
	rm -rf -- "$(APPENGINE_PACKAGES_DIR)"
	rm -rf -- "$(APPENGINE_ENV_DIR)"

$(APPENGINE_ENV_DIR) :
	virtualenv "$(APPENGINE_ENV_DIR)"
	source "$(APPENGINE_ENV_DIR)/bin/activate"; \
		pip install -U pip

appengine_virtualenv : $(APPENGINE_ENV_DIR)

$(APPENGINE_PACKAGES_DIR) : $(APPENGINE_ENV_DIR)
	mkdir -p $(APPENGINE_PACKAGES_DIR)
	source "$(APPENGINE_ENV_DIR)/bin/activate"; \
		pip install --no-deps -r "$(APPENGINE_REQUIREMENTS_TXT)" --target "$(APPENGINE_PACKAGES_DIR)"
	cd "$(APPENGINE_PACKAGES_DIR)/webassets"; \
		patch -p3 < "${PREFIX}/extras/webassets__fix_builtin_filter_loading.diff"
	cd "$(APPENGINE_PACKAGES_DIR)/sqlalchemy"; \
		patch -p3 < "${PREFIX}/extras/sqlalchemy__fix_gaerdbms_exceptions.diff"

appengine_packages : $(APPENGINE_PACKAGES_DIR)

$(APPENGINE_PACKAGES_ZIP) : $(APPENGINE_PACKAGES_DIR)
	cd "$(APPENGINE_PACKAGES_DIR)"; \
		find . -name "*.pyc" -delete; \
		find . -name "*.egg-info" | xargs rm -rf; \
		zip -9rv "../packages.zip.tmp" .; \
		touch "../packages.zip.tmp"; \
		mv "../packages.zip.tmp" "$(APPENGINE_PACKAGES_ZIP)"

appengine_packages_zip : $(APPENGINE_PACKAGES_ZIP)

appengine : appengine_sdk appengine_packages appengine_packages_zip

clean_appengine : clean_appengine_sdk clean_appengine_packages

clean : clean_appengine
