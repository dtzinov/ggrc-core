from ggrc import db
from sqlalchemy import event
from sqlalchemy.sql.expression import text
from sqlalchemy.schema import DDL
from .sql import SqlIndexer

class MysqlRecordProperty(db.Model):
  __tablename__ = 'fulltext_record_properties'
  __table_args__ = {'mysql_engine': 'myisam'}

  key = db.Column(db.Integer, primary_key=True)
  type = db.Column(db.String(64), primary_key=True)
  tags = db.Column(db.String)
  property = db.Column(db.String(64), primary_key=True)
  content = db.Column(db.Text)

event.listen(
    MysqlRecordProperty.__table__,
    'after_create',
    DDL('ALTER TABLE {tablename} ADD FULLTEXT INDEX {tablename}_text_idx '
      '(content)'.format(tablename=MysqlRecordProperty.__tablename__))
    )

class MysqlIndexer(SqlIndexer):
  record_type = MysqlRecordProperty

  def search(self, terms):
    return db.session.query(self.record_type).filter(
      'match (content) against (:terms)').params(terms=terms).all()

