****
GGRC
****

Requirements
============

The following software is required to stand up a GGRC-Core development
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

Getting started with GGRC-Core development should be fast and easy once you
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

Details
=======

GGRC-Core provides both a ``Vagrantfile`` and a ``Cheffile`` to make standing
up a development environment simple and repeatable thanks to the magic of
Vagrant, Chef, and librarian-chef. Vagrant enables developers to use a
consistent and shared VM configuration to perform application testing while
allowing developers to use the source code editing environment of their choice.
The librarian-chef gem provides management of the Chef cookbooks required to
provision the development VM,  with required packages.

Gotchas
=======

After sync'ing your local clone of GGRC-Core you may experience a failure when
trying to run the application due to a change (usually an addition) to the
prerequisites. 

There are two broad classes of requirements for GGRC-Core: cookbooks and Python
packages. Cookbooks are managed via specification in the ``Cheffile`` while
Python packages are managed via specification in ``src/requirements.txt`` for
use with ``pip``.

Most requirements changes should be in ``src/requirements.txt`` and would
exhibit themselves as module import failures.

Changes to ``src/requirements.txt``
-----------------------------------

The first thing to try to resolve issues due to missing prerequisites is to
issue is the following command from within the project directory:

.. sourcecode:: bash

   vagrant provision

This will prompt vagrant to run the Chef provisioner. The result of this
command *should* be an update to the ``/opt/packages.zip`` containing the
Python packages required by the application. However, this may not be the case
and you may experience a provisioning failure due to a change to ``Cheffile``.

Cheffile Changes
----------------

The addition of cookbooks to the project prerequisites can lead to provisioning
failures. The solution is to update the cookbooks in the ``cookbooks``
directory by issuing the following commands from within the project directory:

.. sourcecode:: bash

   librarian-chef install
   vagrant provision

