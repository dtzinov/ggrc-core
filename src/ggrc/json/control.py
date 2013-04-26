from .common import Builder

class Control(Builder):
  _simple_attrs = [
      'version',
      'documentation_description',
      'fraud_related',
      'key_control',
      'active',
      'notes',
      ]
