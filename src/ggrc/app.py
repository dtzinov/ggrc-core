from . import settings

# Initialize Flask app
from flask import Flask

app = Flask('ggrc', instance_relative_config=True)
app.config.from_object(settings)

# Configure Flask-SQLAlchemy for app
from . import db
db.app = app
db.init_app(app)

# Configure webassets for app
from . import assets
app.jinja_env.add_extension('webassets.ext.jinja2.AssetsExtension')
app.jinja_env.assets_environment = assets.environment

# Configure Jinja2 extensions for app
app.jinja_env.add_extension('jinja2.ext.autoescape')
app.jinja_env.add_extension('jinja2.ext.with_')
app.jinja_env.add_extension('hamlpy.ext.HamlPyExtension')

# Initialize services
import ggrc.services
ggrc.services.init_all_services(app)

# Initialize views
import ggrc.views
ggrc.views.init_all_object_views(app)

# Configure Flask-Jasmine, for dev mode unit testing
from flask.ext.jasmine import Jasmine, Asset
jasmine = Jasmine(app)

jasmine.sources(
    Asset("dashboard-js"),
    Asset("dashboard-js-spec-helpers")
)

jasmine.specs(
    Asset("dashboard-js-specs")
)
