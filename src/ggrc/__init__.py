import sys
sys.path.insert(0, 'packages.zip')

from .bootstrap import app, db
from .services.categories import Category, CategoriesCollection

CategoriesCollection.add_to(app, '/api/categories')
Category.add_to(app, '/api/categories/<category_id>')

@app.route("/")
def hello():
  return 'Hello World!'
