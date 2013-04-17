from ggrc import db
from .mixins import Base

class Categorization(Base, db.Model):
  __tablename__ = 'categorizations'

  category_id = db.Column(
      db.Integer, db.ForeignKey('categories.id'), primary_key=True)
  # TODO: Polymorphic association
  categorizable_id = db.Column(db.Integer, primary_key=True)
  categorizable_type = db.Column(db.String, primary_key=True)
