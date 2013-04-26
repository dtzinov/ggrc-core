from .bootstrap import app, db, logger

logger.info("Creating the database")
db.create_all()

from .services import (
    Category, Control,
    )

Category.add_to(app, '/api/categories')
Control.add_to(app, '/api/controls')

@app.route("/")
def hello():
  return 'Hello World!'
