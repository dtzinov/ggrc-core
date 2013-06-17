..
  Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: david@reciprocitylabs.com
  Maintained By: david@reciprocitylabs.com

***********************************
Workflow and Source Code Management
***********************************

gGRC-Core developers use `Pivotal Tracker <https://www.pivotaltracker.com/>`_
for project planning and bug tracking.  The Pivotal Tracker
`gGRC - Python <https://www.pivotaltracker.com/s/projects/593777>`_
project contains the sprint plans and bugs for gGRC-Core.

gGRC-Core developers use the `HubFlow <http://datasift.github.io/gitflow/>`_
tools to automate elements of using feature branches to develop and deliver
features.

General Workflow
================

  #. Begin working on a Pivotal Tracker task by clicking the *'Start'* button.
  #. Start a new feature branch for the work by issuing the following on the
     command line:

       .. sourcecode:: bash
       
          git hf feature start feature_name

  #. Keep up to date with develop by issuing the following commands:

       .. sourcecode:: bash

          git hf update
          git hf feature rebase

     Though, if you are collaborating on a feature branch, a feature pull to
     keep up to date with collaborators will be required and feature merge
     should be preferred to rebase as follows:

       .. sourcecode:: bash

          git hf update
          git hf feature pull
          git hf feature merge

  #. Make required changes and push them to the feature branch on GitHub by
     issuing the following on the command line:

       .. sourcecode:: bash

          git hf feature push

  #. Once the feature or bug fix is complete it must be submitted for code
     review as follows:
     
       .. sourcecode:: bash

          git hf feature submit

     This will create a GitHub pull request from the feature branch to the
     develop branch. Another gGRC-Core developer *should* review and accept,
     reject, or ask other developers for more comments. Developers **should not**
     Gccept their own pull requests.

  #. Once a feature branch pull request has been accepted and merged into
     develop the feature branch should be deleted by issuing the following:

       .. sourcecode:: bash

         git hf feature finish

     Occassionally the local branch won't be deleted and an error message will
     suggest a command to delete the local branch. It should be used, as
     follows:

      .. sourcecode:: bash

         git branch -D feature_name

  #. Click the 'Finish' button on the relevant Pivotal Tracker item. If the
     item was a chore, congratulations, you're done! If the item was a feature
     or bug it will also need to be *delivered*.
     
     If the pull request was accepted then the code was merged into develop and
     should have been deployed to the Continuous Integration environment and
     has been *delivered*. Push the 'Delivered' button to indicate that the
     feature or bug is ready for testing on the Continuous Integration
     instance of gGRC-Core.

Gotchas
=======

Occasionally a raw git command may be executed that places the developers
local feature branch in an undesirable state. For example, issuing a
``git pull`` can result a merge from origin that wasn't intended. The following
command may resolve the problem but must be used with care if you have local
changes that you wish to preserve:

.. sourcecode:: bash

   git reset --hard



