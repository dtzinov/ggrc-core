from ggrc import db
from sqlalchemy import event
from sqlalchemy.schema import DDL
from .sql import SqlIndexer

class MysqlRecordProperty(db.Model):
  __tablename__ = 'fulltext_record_properties'
  __table_args__ = {'mysql_engine': 'myisam'}

  key = db.Column(db.String, primary_key=True)
  type = db.Column(db.String)
  tags = db.Column(db.String)
  property = db.Column(db.String, index=True)
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
    return db.session.query(self.record_type).execute(
        'select key from {tablename} where match (content) against ({terms})'\
            .format(
              tablename=self.record_type.__tablename__,
              terms=terms,
              ))

