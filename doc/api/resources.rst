*********
Resources
*********

There are a broad variety of base GGRC resources. These resources represent
the compliance programs, controls, audit cycles, and other resources
comprising a governance, risk, and compliance solution within an organization.

There is a common pattern of representation followed by all base GGRC
resources following this specification.

Resource Collections
====================

All resources of a specific type are contained in a collection.  Some
properties of the collection resource will be specific to the resource type
and will be indicated as templated fields using the notation
``{property-name}``.

All collections are represented as JSON with Content-Type
``application/json``.

.. list-table:: JSON Representation
   :widths: 30 10 60
   :header-rows: 1

   * - Property
     - Type
     - Description
   * - ``{collection-name}``
     - object
     - The root, collection, object
   * - ``{collection-name}.selfLink``
     - string
     - The URL of the collection resource, itself.
   * - ``{collection-name}.{resource-plural}``
     - array
     - The list of all resources in the collection. Every item in the list is
       an object representation of the resource type contained by the
       collection.

Common Resource Properties
==========================

All GGRC base resources provide the following set of common properties.

.. list-table:: Common Resource Properties
   :widths: 30 10 60
   :header-rows: 1

   * - Property
     - Type
     - Description
   * - ``selflink``
     - string
     - The URL of the resource, itself.
   * - ``viewLink``
     - string
     - *OPTIONAL* URL of the HTML view for the resource.

All GGRC Resource Types
=======================

..
  This should be built off of a directory containing the specs for all of
  resource types.

