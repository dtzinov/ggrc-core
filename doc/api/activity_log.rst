.. _ActivityLogResource:

*********************
Activity Log Resource
*********************

An activity log resource represents changes made to GGRC resources resulting
from an atomic HTTP POST, PUT, or DELETE request. The activity log resource
is intended to provide a feed of events that occur in GGRC for display to
users.

An activity log resource has a media type of ``application/json`` and is an
object containing an :ref:`ActivityLog` object.

Example
=======

.. sourcecode:: javascript

   {
     "activitylog": {
       "selfLink": "/api/activitylog",
       "entries": [
         {
           "selfLink": "/api/activitylog/1000",
           "http_method": "PUT",
           "resourceLink": "/api/programs/12",
           "resource_id": "12",
           "resource_type": "Program",
           "timestamp": "2013-05-30T17:14:00Z",
           "userid": "david@reciprocitylabs.com",
           "revisions": [
             {
               "selfLink": "/api/program_directives/56/revisions/3333",
               "resourceLink": "/api/program_directives/56",
               "contentLink": "/api/program_directives/revisions/3333/content",
               "previousLink": null,
               "timestamp": "2013-05-30T17:14:00Z",
               "modifiedBy": "david@reciprocitylabs.com",
               "action": "created",
               "activityLink": "/api/activitylog/1000",
               "summary": "david@reciprocitylabs.com added Directive 56 to Program 12."
             }
           ]
         }
       ]
     }
   }

Activity Log Content
====================

.. list-table::
   :widths: 20 10 70
   :header-rows: 1

   * - Property
     - Type
     - Description
   * - ``activitylog``
     - object
     - Root property for the activity log resource, an :ref:`ActivityLog`
       object.

.. _ActivityLog:

ActivityLog
===========

.. list-table::
   :widths: 30 10 60
   :header-rows: 1

   * - Property
     - Type
     - Description
   * - ``selfLink``
     - string
     - The url of this resource.
   * - ``entries``
     - array
     - A list of :ref:`ActivityEntry`.

.. _ActivityEntry:

ActivityEntry
-------------

.. list-table::
   :widths: 20 10 70
   :header-rows: 1

   * - Property
     - Type
     - Description
   * - ``selfLink``
     - string
     - URL of the activity entry resource.
   * - ``http_method``
     - string
     - The HTTP method for the recorded activity.
   * - ``resourceLink``
     - string
     - URL of the resource to which the request was made.
   * - ``resource_id``
     - string
     - ID of the target resource.
   * - ``resource_type``
     - string
     - Type name of the target resource.
   * - ``timestamp``
     - string
     - ISO 8601 formatted UTC timestamp indicating the time this activity was
       performed.
   * - ``userid``
     - string
     - Authenticated User ID on whose behalf the request was performed.
   * - ``revisions``
     - array
     - List of :ref:`RevisionEntry` for resources modified as part of the
       transaction satisfying the request.

