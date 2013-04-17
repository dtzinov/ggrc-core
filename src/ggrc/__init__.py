from .bootstrap import app, db, logger

logger.info("Creating the database")
db.create_all()

from .services.categories import Category

Category.add_to(app, '/api/categories')

@app.route("/")
def hello():
  return 'Hello World!'
