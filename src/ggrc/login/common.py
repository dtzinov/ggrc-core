"""Handle the interface to GGRC models for all login methods.
"""

from ggrc import db
from ggrc.models.person import Person

def find_user_by_id(id):
  """Find Person object by some ``id``.
  Note that ``id`` need not be Person().id, but should match the value
  returned by ``Person().get_id()``.
  """
  return Person.query.filter(Person.id==int(id)).first()

def find_user_by_email(email):
  return Person.query.filter(Person.email==email).first()

def create_user(email, **kwargs):
  user = Person(email=email, **kwargs)
  db.session.add(user)
  db.session.commit()
  return user

def find_or_create_user_by_email(email, **kwargs):
  user = find_user_by_email(email)
  if not user:
    user = create_user(email, **kwargs)
  return user

def get_next_url(request, default_url):
  if 'next' in request.args:
    next_url = request.args['next']
    return next_url
  else:
    return default_url
