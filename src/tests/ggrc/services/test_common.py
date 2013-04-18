import ggrc
import time
from datetime import datetime
from flask.ext.testing import TestCase
from ggrc.models.mixins import Base
from ggrc.services.common import Resource
from wsgiref.handlers import format_date_time

class MockModel(Base, ggrc.db.Model):
  __tablename__ = 'test_model'

class MockResourceService(Resource):
  _model = MockModel

  def attrs_for_json(self, object):
    return {'modified_by_id': unicode(object.modified_by_id), }

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

  def mock_json(self, model):
    format = '%Y-%m-%dT%H:%M:%S'
    updated_at = unicode(model.updated_at.strftime(format))
    created_at = unicode(model.created_at.strftime(format))
    return {
        u'id': model.id,
        u'selfLink': unicode(URL_MOCK_RESOURCE.format(model.id)),
        u'modified_by_id': unicode(model.modified_by_id),
        u'updated_at': updated_at,
        u'created_at': created_at,
        }

  def mock_model(self, **kwarg):
    mock = MockModel(**kwarg)
    ggrc.db.session.add(mock)
    ggrc.db.session.commit()
    return mock

  def http_timestamp(self, timestamp):
    return format_date_time(time.mktime(timestamp.utctimetuple()))

  def assertRequiredHeaders(
      self, response, headers={'Content-Type': 'application/json',}):
    self.assertIn('Etag', response.headers)
    self.assertIn('Last-Modified', response.headers)
    self.assertIn('Content-Type', response.headers)
    for k,v in headers.items():
      self.assertEquals(v, response.headers.get(k))

  def test_empty_collection_get(self):
    response = self.client.get(self.mock_url())
    self.assert200(response)

  def test_missing_resource_get(self):
    response = self.client.get(self.mock_url('foo'))
    self.assert404(response)

  def test_collection_get(self):
    date1 = datetime(2013, 4, 17, 0, 0, 0, 0)
    date2 = datetime(2013, 4, 20, 0, 0, 0, 0)
    mock1 = self.mock_model(
        modified_by_id=42, created_at=date1, updated_at=date1)
    mock2 = self.mock_model(
        modified_by_id=43, created_at=date2, updated_at=date2)
    response = self.client.get(self.mock_url())
    self.assert200(response)
    self.assertRequiredHeaders(
        response,
        { 'Last-Modified': self.http_timestamp(date2),
          'Content-Type': 'application/json',
        })
    self.assertIn('test_model_collection', response.json)
    self.assertEqual(2, len(response.json['test_model_collection']))
    self.assertIn('selfLink', response.json['test_model_collection'])
    self.assertIn('test_model', response.json['test_model_collection'])
    collection = response.json['test_model_collection']['test_model']
    self.assertEqual(2, len(collection))
    self.assertDictEqual(self.mock_json(mock2), collection[0])
    self.assertDictEqual(self.mock_json(mock1), collection[1])

  def test_resource_get(self):
    date1 = datetime(2013, 4, 17, 0, 0, 0, 0)
    mock1 = self.mock_model(
        modified_by_id=42, created_at=date1, updated_at=date1)
    response = self.client.get(self.mock_url(mock1.id))
    self.assert200(response)
    self.assertRequiredHeaders(
      response,
      { 'Last-Modified': self.http_timestamp(date1),
        'Content-Type': 'application/json',
      })
    self.assertIn('mockmodel', response.json)
    self.assertDictEqual(self.mock_json(mock1), response.json['mockmodel'])
