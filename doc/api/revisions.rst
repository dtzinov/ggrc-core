..
  Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: david@reciprocitylabs.com
  Maintained By: david@reciprocitylabs.com


.. _ResourceRevisions:

******************
Resource Revisions
******************

A revision history is maintained for every base GGRC resource type. The
revision history for a particular resource can be retrieved as a collection
that points to the individual revisions for that resource.

Revisions Collection Resource
=============================

Example
-------

.. sourcecode:: javascript

   {
     "revisions": {
       "selfLink": "/api/programs/56/revisions",
       "entries": [
         {
           "selfLink": "/api/programs/56/revisions/1234",
           "resourceLink": "/api/programs/56",
           "contentLink": "/api/programs/56/revisions/1234/content",
           "previousLink": "/api/programs/56/revisions/1111",
           "timestamp": "2013-05-30T11:11:11Z",
           "modifiedBy": "david@reciprocitylabs.com",
           "action": "modified",
           "activityLink": "/api/activitylog/11",
           "summary": null
         },
         {
           "selfLink": "/api/programs/56/revisions/1111",
           "resourceLink": "/api/programs/56",
           "contentLink": "/api/programs/56/revisions/1111",
           "previousLink": null,
           "timestamp": "2013-05-30T00:00:00Z",
           "modifiedBy": "david@reciprocitylabs.com",
           "action": "created",
           "activityLink": "/api/activitylog/10",
           "summary": null
         }
       ]
     }
   }

Revisions Collection Content
----------------------------

.. list-table::
   :widths: 30 10 60
   :header-rows: 1

   * - Property
     - Type
     - Description
   * - ``revisions``
     - object
     - Root property for a revisions collection, an :ref:`RevisionsCollection`
       object.

.. _RevisionsCollection:

RevisionsCollection
-------------------

.. list-table::
   :widths: 30 10 60
   :header-rows: 1

   * - Property
     - Type
     - Description
   * - ``selfLink``
     - string
     - The URL of this resource.
   * - ``resourceLink``
     - string
     - The URL of the resource whose revision history is contained in this
       revision collection.
   * - ``entries``
     - array
     - The list of all revisions for the resource as :ref:`RevisionEntry`
       objects.

Revision Entry Resource
=======================

A Revision Entry Resource is a single entry containing the details of a
particular revision.

Example
-------

.. sourcecode:: javascript

   {
     "revision": {
       "selfLink": "/api/programs/56/revisions/1234",
       "resourceLink": "/api/programs/56",
       "contentLink": "/api/programs/56/revisions/1234/content",
       "previousLink": "/api/programs/56/revisions/1111",
       "timestamp": "2013-05-30T11:11:11Z",
       "modifiedBy": "david@reciprocitylabs.com",
       "deleted": false,
       "activityLink": "/api/activitylog/11",
       "summary": null
     }
   }

Revision Entry Content
----------------------

.. list-table::
   :widths: 20 10 70
   :header-rows: 1

   * - Property
     - Type
     - Description
   * - ``revision``
     - object
     - Root property for a revision resource, a :ref:`RevisionEntry` object.

.. _RevisionEntry:

RevisionEntry
=============

.. list-table::
   :widths: 30 10 60
   :header-rows: 1

   * - Property
     - Type
     - Description
   * - ``selfLink``
     - string
     - URL of this revision entry resource.
   * - ``resourceLink``
     - string
     - URL of the resource modified as a result of an HTTP request.
   * - ``contentLink``
     - string
     - The URL for this specific revision of the resource. If ``action`` is
       ``deleted`` the value **MUST** be ``null``.
   * - ``previousLink``
     - string
     - URL of the :ref:`RevisionEntry` for the previous revision of the
       resource.  If ``action`` is ``created`` the the value **MUST** be
       ``null``.
   * - ``timestamp``
     - string
     - ISO 8601 formatted UTC timestamp indicating the time this revision was
       created.
   * - ``modifiedBy``
     - string
     - The userid recorded when the revision was created.
   * - ``action``
     - string 
     - **MUST** be one of ``created``, ``modified``, or ``deleted``.
   * - ``activityLink``
     - string
     - The URL of the activity log resource for the atomic HTTP transaction
       that created this revision.
   * - ``summary``
     - string
     - **OPTIONAL** text summary of changes to the resource intended for
       display to users. If a summary isn't provided or isn't available the
       value **MUST** be ``null``.

Revision Resource
=================

The revision resource content will depend upon the type of resource. HTTP GET
of a revision resource should return an HTTP response that contains the same
representation of the resource that would have been returned when the revision
was the current revision. Proper HTTP headers should also be returned with an
appropriate Etag, Last-Modified, and caching header values.

.. note::

   There is no revision history provided for a GGRC collection resource, there
   are only revision histories provided for resources contained in the
   collection.

..
  Add a link to the resources document so that they can be referenced for the
  content that could be found in a resource of any given type.

  Also, should specify a special ``X-GGRC-revision`` header for the URL of the
  revision entry for the revision. That way - you can get that given a
  resource revision URL.
