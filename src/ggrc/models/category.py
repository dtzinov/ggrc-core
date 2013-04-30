from ggrc import db
from sqlalchemy.ext.associationproxy import association_proxy
from .categorization import Categorization
from .mixins import Base, Hierarchical

class Category(Base, Hierarchical, db.Model):
  __tablename__ = 'categories'

  name = db.Column(db.String)
  lft = db.Column(db.Integer)
  rgt = db.Column(db.Integer)
  scope_id = db.Column(db.Integer)
  depth = db.Column(db.Integer)
  required = db.Column(db.Boolean)

  categorizations = db.relationship(
      'ggrc.models.categorization.Categorization',
      backref='category',
      )
  control_categorizations = db.relationship(
      'Categorization',
      primaryjoin=\
          'and_(foreign(Categorization.category_id) == Category.id, '
               'foreign(Categorization.categorizable_type) == "Control")',
      )
  risk_categorizations = db.relationship(
      'Categorization',
      primaryjoin=\
          'and_(foreign(Categorization.category_id) == Category.id, '
               'foreign(Categorization.categorizable_type) == "Risk")',
      )
  controls = association_proxy(
      'control_categorizations', 'categorizable',
      creator=lambda categorizable: Categorization(
          categorizable=categorizable,
          modified_by_id=1,
          categorizable_type='Control',
          ),
      )
  risks = association_proxy(
      'risk_categorizations', 'categorizable',
      creator=lambda categorizable: Categorization(
          categorizable=categorizable,
          modified_by_id=1,
          categorizable_type='Risk',
          ),
      )

  # REST properties
  _publish_attrs = [
      'name',
      'required',
      'categorizations',
      'control_categorizations',
      'risk_categorizations',
      'controls',
      'risks',
      ]
  _update_attrs = [
      'name',
      'required',
      ]
