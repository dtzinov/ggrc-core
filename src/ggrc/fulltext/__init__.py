class Indexer(object):
  def create_record(self, record):
    raise NotImplementedError()

  def update_record(self, record):
    raise NotImplementedError()

  def delete_record(self, key):
    raise NotImplementedError()

  def search(self, terms):
    raise NotImplementedError()

class Record(object):
  def __init__(self, key, type, tags, **kwargs):
    self.key = key
    self.type = type
    self.tags = tags
    self.properties = kwargs

def get_indexer(indexer=[]):
  if not indexer:
    import sys
    from ggrc import settings
    indexer_name = \
        settings.FULLTEXT_INDEXER or 'ggrc.fulltext.sqlite.Sqlite3Indexer'
    idx = indexer_name.rfind('.')
    module_name = indexer_name[0:idx]
    class_name = indexer_name[idx+1:]
    __import__(module_name)
    module = sys.modules[module_name]
    indexer.append(getattr(module, class_name)())
  return indexer[0]

