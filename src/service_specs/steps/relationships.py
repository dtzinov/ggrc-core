@given('a RelationshipType "{name}" forward phrase "{fwd}"')
def create_relationship_type(context, name, fwd):
  from ggrc import db
  from ggrc.models.relationship import RelationshipType
  t = RelationshipType(
      relationship_type=name,
      forward_phrase=fwd,
      symmetric=False,
      )
  db.session.add(t)
  db.session.commit()

@given('a symmetric RelationshipType "{name}" forward phrase "{fwd}" and '
       'backward phrase "{back}"')
def create_relationship_type(context, name, fwd, back):
  from ggrc import db
  from ggrc.models.relationship import RelationshipType
  t = RelationshipType(
      relationship_type=name,
      forward_phrase=fwd,
      backward_phrase=back,
      symmetric=True,
      )
  db.session.add(t)
  db.session.commit()

