from ggrc import db
from . import Indexer

class SqlIndexer(Indexer):
  def create_record(self, record, commit=True):
    for k,v in record.properties.items():
      db.session.add(self.record_type(
        key=record.key,
        type=record.type,
        tags=record.tags,
        property=k,
        content=v,
        ))
    if commit:
      db.session.commit()

  def update_record(self, record):
    self.delete_record(record.key, commit=False)
    self.create_record(record, commit=True)

  def delete_record(self, key, commit=True):
    db.session.query(self.record_type).filter(\
        self.record_type.key == key).delete()
    if commit:
      db.session.commit()

