from ggrc import db
from sqlalchemy.ext.declarative import declared_attr
from .associationproxy import association_proxy
from .mixins import BusinessObject, Timeboxed
from .categorization import Categorizable
from .object_document import Documentable
from .object_person import Personable

CATEGORY_SYSTEM_TYPE_ID = 101

class SystemCategorized(Categorizable):
  @declared_attr
  def categorizations(cls):
    return cls._categorizations(
        'categorizations', 'categories', CATEGORY_SYSTEM_TYPE_ID)

class System(
    Documentable, Personable, Timeboxed, SystemCategorized,
    BusinessObject, db.Model):
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
  controls = association_proxy('system_controls', 'control', 'SystemControl')
  responses = db.relationship('Response', backref='system')
  #TODO What about system_section?
  owner = db.relationship('Person', uselist=False)
  sub_system_systems = db.relationship(
      'SystemSystem', foreign_keys='SystemSystem.parent_id', backref='parent')
  sub_systems = association_proxy(
      'sub_system_systems', 'child', 'SystemSystem')
  super_system_systems = db.relationship(
      'SystemSystem', foreign_keys='SystemSystem.child_id', backref='child')
  super_systems = association_proxy(
      'super_system_systems', 'parent', 'SystemSystem')
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
      'is_biz_process',
      'type',
      'version',
      'notes',
      'network_zone',
      'system_controls',
      'controls',
      'responses',
      'owner',
      'sub_system_systems',
      'sub_systems',
      'super_system_systems',
      'super_systems',
      'transactions',
      ]
  _update_attrs = [
      'infrastructure',
      'is_biz_process',
      'type',
      'version',
      'notes',
      'network_zone',
      'controls',
      'responses',
      'owner',
      'sub_systems',
      'super_systems',
      'transactions',
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(System, cls).eager_query()
    return query.options(
        orm.joinedload('type'),
        orm.joinedload('network_zone'),
        orm.subqueryload('responses'),
        orm.subqueryload_all('system_controls.control'),
        orm.subqueryload_all('sub_system_systems.child'),
        orm.subqueryload_all('super_system_systems.parent'),
        orm.subqueryload('transactions'))
