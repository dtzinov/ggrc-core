from ggrc import db
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from .mixins import BusinessObject, Timeboxed
from .categorization import Categorizable

CATEGORY_SYSTEM_TYPE_ID = 101

class SystemCategorized(Categorizable):
  @declared_attr
  def categorizations(cls):
    return cls._categorizations(
        'categorizations', 'categories', CATEGORY_SYSTEM_TYPE_ID)

class System(Timeboxed, BusinessObject, SystemCategorized, db.Model):
  __tablename__ = 'systems'

  infrastructure = db.Column(db.Boolean)
  # TODO: unused?
  owner_id = db.Column(db.Integer, db.ForeignKey('people.id'))
  is_biz_process = db.Column(db.Boolean, default=False)
  # TODO: handle option
  type_id = db.Column(db.Integer)
  version = db.Column(db.String)
  notes = db.Column(db.Text)
  # TODO: handle option
  network_zone_id = db.Column(db.Integer)
  system_controls = db.relationship('SystemControl', backref='system')
  controls = association_proxy('system_controls', 'control')
  responses = db.relationship('Response', backref='system')
  #TODO What about system_section?
  owner = db.relationship('Person', uselist=False)
  sub_system_systems = db.relationship(
      'SystemSystem', foreign_keys='SystemSystem.parent_id', backref='parent')
  sub_systems = association_proxy('sub_system_systems', 'parent')
  super_system_systems = db.relationship(
      'SystemSystem', foreign_keys='SystemSystem.child_id', backref='child')
  super_systems = association_proxy('super_system_systems', 'child')
  transactions = db.relationship('Transaction', backref='system')
  type = db.relationship(
      'Option',
      primaryjoin='and_(foreign(System.type_id) == Option.id, '\
                       'Option.role == "system_type")',
      uselist=False,
      )
  network_zone = db.relationship(
      'Option',
      primaryjoin='and_(foreign(System.network_zone_id) == Option.id, '\
                       'Option.role == "network_zone")',
      uselist=False,
      )

  # REST properties
  _publish_attrs = [
      'infrastructure',
      #'owner_id, this should probably be a "Person"
      'is_biz_process',
      #'type_id', this should be a Type
      'version',
      'notes',
      #'network_zone_id',
      ]
