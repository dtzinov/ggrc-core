"""Manage "static" assets

The actual list of stylesheets and javascripts to compile is in 
`assets/assets.yaml`.

When developing, you can use `webassets` to automatically recompile changed
assets by starting the `webassets` command-line utility:

..
  cd src/ggrc
  webassets -m ggrc.assets watch

Currently, Compass/Sass is used to build CSS assets, and it has its own
monitor utility, which can be invoked thusly:

..
  cd src/ggrc
  compass watch -c assets/compass.config.rb
"""

from . import settings

# Initialize webassets to handle the asset pipeline
import webassets

environment = webassets.Environment()

environment.manifest = 'file:assets.manifest'
environment.versions = 'hash:32'

import webassets.updater
environment.updater = webassets.updater.TimestampUpdater()

# Read asset listing from YAML file
import os, yaml
assets_yaml_path = os.path.join(settings.MODULE_DIR, 'assets', 'assets.yaml')
with open(assets_yaml_path) as f:
  asset_paths = yaml.load(f.read())

environment.url = '/static'
environment.directory = 'static'

environment.load_path = [
  'assets/javascripts',
  'assets/vendor/javascripts',
  'assets/vendor/bootstrap-sass/vendor/assets/javascripts',
  'assets/vendor/remoteipart/vendor/assets/javascripts',
  'assets/stylesheets',
  'assets/vendor/stylesheets',
  'assets/js_specs',
  ]

environment.register("dashboard-js", webassets.Bundle(
  *asset_paths['dashboard-js-files'],
  #filters='jsmin',
  output='dashboard-%(version)s.js'))

environment.register("dashboard-css", webassets.Bundle(
  *asset_paths['dashboard-css-files'],
  output='dashboard-%(version)s.css'))

environment.register("dashboard-js-specs", webassets.Bundle(
  *asset_paths['dashboard-js-spec-files'],
  #filters='jsmin',
  output='dashboard-%(version)s-specs.js'))

environment.register("dashboard-js-spec-helpers", webassets.Bundle(
  *asset_paths['dashboard-js-spec-helpers'],
  #filters='jsmin',
  output='dashboard-%(version)s-spec-helpers.js'))