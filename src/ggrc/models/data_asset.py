from .mixins import Slugged, Timeboxed, Hyperlinked

class DataAsset(Slugged, Timeboxed, Hyperlinked, db.Model):
  __tablename__ = 'data_assets'

