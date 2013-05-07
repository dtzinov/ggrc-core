import ggrc.builder
import ggrc.models
from ggrc.builder.json import publish
from ggrc.services.common import Resource
from mock import MagicMock
from tests.ggrc import TestCase

class TestBuilder(TestCase):
  '''Note: Since we are using module member lookup to wire the builders up,
  we have to clean up after every test. This is why we're using mock and
  removing the builders on tearDown.
  '''
  def mock_service(self, name):
    svc = MagicMock(Resource)
    svc.url_for.return_value = '/some-url'
    self.mock_services[name] = svc
    setattr(ggrc.services, name, svc)
    return svc

  def mock_class(self, name, bases=(), _publish_attrs=None):
    cls = MagicMock()
    cls.__name__ = name
    cls.__bases__ = bases
    if _publish_attrs:
      cls._publish_attrs = _publish_attrs
    self.mock_builders.append(name)
    return cls

  def mock_model(self, name, bases=(), _publish_attrs=None, **kwarg):
    model = MagicMock()
    model.__class__ = self.mock_class(name, bases, _publish_attrs)
    for k,v in kwarg.items():
      setattr(model, k, v)
    return model

  def setUp(self):
    super(TestBuilder, self).setUp()
    self.mock_services = {}
    self.mock_builders = []

  def tearDown(self):
    for k in self.mock_services.keys():
      delattr(ggrc.services, k)
    for k in self.mock_builders:
      delattr(ggrc.builder.json, k) if hasattr(ggrc.builder.json, k) else None
    super(TestBuilder, self).tearDown()

  def test_simple_builder(self):
    self.mock_service('MockModel')
    model = self.mock_model(
        'Mock_test_simple_builder',
        foo='bar',
        id=1,
        _publish_attrs=['foo'],
        )
    json_obj = publish(model)
    self.assertIn('foo', json_obj)
    self.assertEqual('bar', json_obj['foo'])

  def test_simple_mixin_inheritance(self):
    self.mock_service('MockModelWithMixin')
    mock_mixin = self.mock_class('MockMixin', _publish_attrs=['boo'])
    model = self.mock_model(
        'MockModelWithMixin',
        bases=(mock_mixin,),
        foo='bar',
        boo='far',
        _publish_attrs=['foo'],
        )
    json_obj = publish(model)
    self.assertDictContainsSubset(
        {'foo': 'bar', 'boo': 'far'},
        json_obj)

  def test_sophisticated_mixins(self):
    self.mock_service('ModelA')
    self.mock_service('ModelB')
    mixin = self.mock_class('Mixin', _publish_attrs=['mixin'])
    mixin_subclass = self.mock_class(
        'MixinSubclass', (mixin,), _publish_attrs=['mixin_subclass'])
    model_a = self.mock_model('ModelA',
        bases=(mixin_subclass,),
        prop_a='prop_a', mixin='mixin_a', mixin_subclass='mixin_subclass_a',
        _publish_attrs=['prop_a'])
    model_b = self.mock_model('ModelB',
        bases=(mixin,), prop_b='prop_b', mixin='mixin_b',
        _publish_attrs=['prop_b'])
    json_obj = publish(model_a)
    self.assertDictContainsSubset(
        {'prop_a': 'prop_a', 'mixin': 'mixin_a',
         'mixin_subclass': 'mixin_subclass_a'},
        json_obj)
    json_obj = publish(model_b)
    self.assertDictContainsSubset(
        {'prop_b': 'prop_b', 'mixin': 'mixin_b'},
        json_obj)
