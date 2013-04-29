import ggrc.json
import ggrc.models
from ggrc.json.common import Builder, publish
from ggrc.services.common import Resource
from mock import MagicMock
from tests.ggrc import TestCase

class TestBuilder(TestCase):
  def mock_service(self, name):
    svc = MagicMock(Resource)
    svc.url_for.return_value = '/some-url'
    self.mock_services[name] = svc
    setattr(ggrc.services, name, svc)
    return svc

  def mock_builder(self, name, simple_attrs=[]):
    class MockBuilder(Builder):
      _publish_attrs = simple_attrs
    self.mock_builders[name] = MockBuilder
    setattr(ggrc.json, name, MockBuilder)
    return MockBuilder

  def mock_class(self, name, bases=()):
    cls = MagicMock()
    cls.__name__ = name
    cls.__bases__ = bases
    return cls

  def mock_model(self, name, bases=(), **kwarg):
    model = MagicMock()
    model.__class__ = self.mock_class(name, bases)
    for k,v in kwarg.items():
      setattr(model, k, v)
    return model

  def setUp(self):
    super(TestBuilder, self).setUp()
    self.mock_services = {}
    self.mock_builders = {}

  def tearDown(self):
    for k in self.mock_services.keys():
      delattr(ggrc.services, k)
    for k in self.mock_builders.keys():
      delattr(ggrc.json, k)
    super(TestBuilder, self).tearDown()

  def test_simple_builder(self):
    self.mock_service('MockModel')
    self.mock_builder('MockModel', ['foo'])
    model = self.mock_model('MockModel', foo='bar')
    json_obj = publish(model)
    self.assertIn('foo', json_obj)
    self.assertEqual('bar', json_obj['foo'])

  def test_simple_mixin_inheritance(self):
    self.mock_service('MockModel')
    self.mock_builder('MockModel', ['foo'])
    self.mock_builder('MockMixin', ['boo'])
    mock_mixin = self.mock_class('MockMixin')
    model = self.mock_model(
        'MockModel', bases=(mock_mixin,), foo='bar', boo='far')
    json_obj = publish(model)
    self.assertDictContainsSubset(
        {'foo': 'bar', 'boo': 'far'},
        json_obj)

  def test_sophisticated_mixins(self):
    self.mock_service('ModelA')
    self.mock_service('ModelB')
    self.mock_builder('ModelA', ['prop_a'])
    self.mock_builder('ModelB', ['prop_b'])
    self.mock_builder('Mixin', ['mixin'])
    self.mock_builder('MixinSubclass', ['mixin_subclass'])
    mixin = self.mock_class('Mixin')
    mixin_subclass = self.mock_class('MixinSubclass', (mixin,))
    model_a = self.mock_model('ModelA',
        bases=(mixin_subclass,),
        prop_a='prop_a', mixin='mixin_a', mixin_subclass='mixin_subclass_a')
    model_b = self.mock_model('ModelB',
        bases=(mixin,), prop_b='prop_b', mixin='mixin_b')
    json_obj = publish(model_a)
    self.assertDictContainsSubset(
        {'prop_a': 'prop_a', 'mixin': 'mixin_a',
         'mixin_subclass': 'mixin_subclass_a'},
        json_obj)
    json_obj = publish(model_b)
    self.assertDictContainsSubset(
        {'prop_b': 'prop_b', 'mixin': 'mixin_b'},
        json_obj)
