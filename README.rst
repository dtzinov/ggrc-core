*********
gGRC-Core
*********

Requirements
============

The following software is required to stand up a gGRC-Core development
environment:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Prerequisite
     - Description
   * - `VirtualBox <https://www.virtualbox.org/>`_
     - Oracle VirtualBox Virtual Machine player
   * - `Vagrant <http://www.vagrantup.com/>`_
     - Handy scriptable VM management
   * - `librarian (ruby gem) <http://rubygems.org/gems/librarian>`_
     - Ruby bundle management framework.
   * - `librarian-chef (ruby gem) <http://rubygems.org/gems/librarian-chef>`_
     - `Opscode Chef <http://www.opscode.com/chef/>`_ cookbook manager.

Quick Start
===========

Getting started with gGRC-Core development should be fast and easy once you
have the prerequisite software installed. Here are the steps:

* clone the repo
* cwd to the project directory
* run the following:

.. sourcecode:: bash

  librarian-chef install
  vagrant up
  vagrant ssh
  cd /vagrant
  ls

Now you're in the VM and ready to rock. Get to work!

Launching gGRC as Stand-alone Flask
-----------------------------------

.. sourcecode:: bash

   cd /vagrant
   ./launch_ggrc

Launching gGRC in Google App Engine SDK
---------------------------------------

.. sourcecode:: bash

   cd /vagrant
   ./launch_gae_ggrc

Accessing the Application
-------------------------

The application will be accessible via this URL: http://localhost:8080/

If you're running the Google App Engine SDK, the App Engine management console
will be avaiable via this URL: http://localhost:8000/

Running Unit Tests
------------------

.. sourcecode:: bash

   cd /vagrant
   ./unittests

Details
=======

gGRC-Core provides both a ``Vagrantfile`` and a ``Cheffile`` to make standing
up a development environment simple and repeatable thanks to the magic of
Vagrant, Chef, and librarian-chef. Vagrant enables developers to use a
consistent and shared VM configuration to perform application testing while
allowing developers to use the source code editing environment of their choice.
The librarian-chef gem provides management of the Chef cookbooks required to
provision the development VM,  with required packages.

Gotchas
=======

After sync'ing your local clone of gGRC-Core you may experience a failure when
trying to run the application due to a change (usually an addition) to the
prerequisites. 

There are two broad classes of requirements for gGRC-Core: cookbooks and
Python packages. Cookbooks are managed via specification in the ``Cheffile``
while Python packages are managed via specification in pip requirements files.

There are two pip requirements files: a runtime requirements file,
``src/requirements.txt``, for application package dependencies and a
development requirements file, ``src/dev-requirements.txt``, for additional
development time package dependencies. The runtime requirements are deployed
with the application while the development requirements are only used in the
development environment (largely for testing purposes).

Most requirements changes should be in either ``src/requirements.txt`` or
``src/dev-requirements.txt`` and would exhibit themselves as module import
failures.

Changes to Requirements Files
-----------------------------

The first thing to try to resolve issues due to missing prerequisites is to
issue is the following command from within the project directory in the host
operating system (what you're running the VM on):

.. sourcecode:: bash

   vagrant provision

This will prompt vagrant to run the Chef provisioner. The result of this
command *should* be an update to the ``/opt/packages.zip`` containing the
Python packages required by the application as well as any updates to the
system Python packages for any new development package requirements. However,
this may not be the case and you may experience a provisioning failure due to
a change to ``Cheffile``.

Cheffile Changes
----------------

The addition of cookbooks to the project prerequisites can lead to provisioning
failures. The solution is to update the cookbooks in the ``cookbooks``
directory by issuing the following commands from within the project directory:

.. sourcecode:: bash

   librarian-chef install
   vagrant provision

