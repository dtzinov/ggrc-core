@given('an Option named "{name}" with role "{role}"')
def create_option(context, name, role):
  named_example_resource(context, 'Option', name, role=role)
