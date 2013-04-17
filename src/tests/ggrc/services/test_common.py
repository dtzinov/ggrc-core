import ggrc
from flask.ext.testing import TestCase
from ggrc.models.mixins import Base
from ggrc.services.common import Resource
from wsgiref.handlers import format_date_time

class MockModel(Base, ggrc.db.Model):
  __tablename__ = 'test_model'

class MockResourceService(Resource):
  _model = MockModel

URL_MOCK_COLLECTION = '/api/mock_resources'
URL_MOCK_RESOURCE = '/api/mock_resources/{}'
MockResourceService.add_to(ggrc.app, URL_MOCK_COLLECTION)

class TestResource(TestCase):
  def setUp(self):
    ggrc.db.create_all()

  def tearDown(self):
    ggrc.db.session.remove()
    ggrc.db.drop_all()

  def create_app(self):
    ggrc.app.testing = True
    ggrc.app.debug = False
    return ggrc.app

  def mock_url(self, resource=None):
    if resource is not None:
      return URL_MOCK_RESOURCE.format(resource)
    return URL_MOCK_COLLECTION

  def test_empty_collection_get(self):
    response = self.client.get(self.mock_url())
    self.assert200(response)

  def test_missing_resource_get(self):
    response = self.client.get(self.mock_url('foo'))
    self.assert404(response)

  def test_collection_get(self):
    mock1 = MockModel(modified_by_id=42)
    mock2 = MockModel(modified_by_id=43)
    ggrc.db.session.add(mock1)
    ggrc.db.session.add(mock2)
    ggrc.db.session.commit()
    response = self.client.get(self.mock_url())
    self.assert200(response)
    self.assertIn('Etag', response.headers)
    self.assertIn('Last-Modified', response.headers)
    self.assertEquals('application/json', response.content_type)
    self.assertIn('test_model_collection', response.json)
    self.assertEqual(2, len(response.json['test_model_collection']))
    #TODO check that the Last-Modified and Etag are correct
    #     Add more tests, like retrieving individual resources
