@given('a Category resource named "{name}" for scope "{scope}"')
def create_category(context, name, scope):
  named_example_resource(context, 'Category', name, scope_id=int(scope))

