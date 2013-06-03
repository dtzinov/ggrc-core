..
  Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: dan@reciprocitylabs.com
  Maintained By: dan@reciprocitylabs.com


Templates
=========

gGRC-core uses HamlPy, Jinja2, and built-in Flask functionality for rendering
templates.


Basic documentation
-------------------

Jinja2: http://jinja.pocoo.org/docs/

HamlPy: https://github.com/jessemiller/HamlPy/blob/master/reference.md

Flask: https://github.com/mitsuhiko/flask/blob/master/docs/templating.rst


gGRC-core additions
-------------------


Style Guide
~~~~~~~~~~~

The styleguide can be found live in the deployment at the "/design" path.


Template Filters
~~~~~~~~~~~~~~~~

``underscore``:
  Changes spaces to underscores and converts everything to lowercase

``nospace_filter``:
  Removes spaces


Context Processors
~~~~~~~~~~~~~~~~~~

``inject_config``:
  Makes Flask application settings available in the templates.
  ``config``: mirrors Flask's ``app.config``
