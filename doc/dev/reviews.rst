..
  Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: david@reciprocitylabs.com
  Maintained By: david@reciprocitylabs.com


****************
Review Documents
****************

gGRC will go under periodic external review to validate appropriate precautions
are taken to ensure that gGRC is following best practices in application
security and protecting user privacy. Records of these reviews must be
maintained and the gGRC project has chosen to keep these records as a part of
the project maintained in the source code repository.

Review documents **MUST** be kept in the ``reviews`` directory of the gGRC
project and **SHOULD** follow this specification.

Review Document Format
======================

Review documents will record the purpose of the review, the reviewers, and the
outcome of the review.

Example
-------

.. sourcecode:: rest

   ***********
   gGRC Review
   ***********

   :Purpose:
      Brief discussion of what is being reviewed and criteria for approval.

   :Reviewers:
      "Reviewer Name" <reviewer-email@example.com>
      "Another Reviewer" <another-email@example.com>

   History
   =======

   YYYY-MM-DD
   ----------
     
   :Status:
     Open | Approved | Rejected

   :Files:
      an-example.file
      some_files/another_example.file

