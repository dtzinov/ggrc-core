from .bootstrap import app, db, logger

logger.info("Creating the database")
db.create_all()

#from ggrc import models
#from .models import *
#from .services import Resource

from .services import (
    Category, Control,
    )

Category.add_to(app, '/api/categories')
Control.add_to(app, '/api/controls')

#Resource.add_to(app, '/api/categories', Category)
#Resource.add_to(app, '/api/controls', Control)

@app.route("/")
def hello():
  return 'Hello World!'
