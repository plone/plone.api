=======================
Development environment
=======================

This section is meant for contributors to the `plone.api` project. Its purpose
is to guide them through the steps needed to start contributing.

.. note ::: This HowTo is written for Linux and OS X users. If you're are
   running Windows we suggest using VMWare or a similar Virtualization tool to
   install Ubuntu Linux on a virtual machine or installing Ubuntu Linux as a
   secondary OS on your machine. Alternatively, you can browse Plone's
   documentation on how to get Plone development environment up and running on
   Windows. Plone does run on Windows but it's not completely trivial to set it
   up.

Prerequisites
=============

System libraries
----------------

First let's look at 'system' libraries and applications that are normally
installed with your OS packet manager, such as apt, aptitude, yum, etc.:

* ``libxml2`` - An xml parser written in C.
* ``libxslt`` - XSLT library written in C.
* ``git`` - Version control system.
* ``gcc`` - The GNU Compiler Collection.
* ``g++`` - The C++ extensions for gcc.
* ``GNU make`` - The fundamental build-control tool.
* ``GNU tar`` - The (un)archiving tool for extracting downloaded archives.
* ``bzip2`` and ``gzip`` decompression packages - ``gzip`` is nearly standard,
  however some platforms will require that ``bzip2`` be installed.
* ``Python 2.7`` - Linux distributions normally already have it, OS X users
  should use https://github.com/collective/buildout.python to get a clean Python
  version (the one that comes with OS X is broken).


Python tools
------------

Then you'll also need to install some Python specific tools:

* easy_install - the Python packaging system (download
  http://peak.telecommunity.com/dist/ez_setup.py and run
  ``sudo python2.7 ez_setup.py``.
* virtualenv - a tool that assists in creating isolated Python working
  environments. Run ``sudo easy_install virtualenv`` after your have installed
  `easy_install` above.

.. note::

    Again, OS X users should use https://github.com/collective/buildout.python,
    it will make your life much easier to have a cleanly compiled Python instead
    of using the system one that is broken in many deeply confusing ways.


Further information
-------------------

If you experience problems read through the following links as almost all of the
above steps are required for a default Plone development environment:

* http://plone.org/documentation/tutorial/buildout
* http://pypi.python.org/pypi/zc.buildout/
* http://pypi.python.org/pypi/setuptools
* http://plone.org/documentation/manual/installing-plone

If you are an OS X user, you first need a working Python implementation (the one
that comes with the operating system is broken). Use
https://github.com/collective/buildout.python and be happy. Also applicable to
other OSes, if getting a working Python proves a challenge.


Creating and using the development environment
==============================================

Go to your projects folder and download the lastest `plone.api` code:

.. sourcecode:: bash

    [you@local ~]$ cd <your_work_folder>
    [you@local work]$ git clone https://github.com/plone/plone.api.git

Now `cd` into the newly created directory and build your environment:

.. sourcecode:: bash

    [you@local work]$ cd plone.api
    [you@local plone.api]$ make

Go make some tea while `make` creates an isolated Python environment in your
``plone.api`` folder,  bootstraps `zc.buildout`, fetches all dependencies,
builds Plone, runs all tests and generates documentation so you can open it
locally later on.

Other commands that you may want to run:

.. sourcecode:: bash

    [you@local plone.api]$ make tests  # run all tests and syntax validation
    [you@local plone.api]$ make docs   # re-generate documentation
    [you@local plone.api]$ make clean  # reset your env back to a fresh start
    [you@local plone.api]$ make        # re-build env, generate docs, run tests

Open ``Makefile`` in your favorite code editor to see all possible commands
and what they do. And read http://www.gnu.org/software/make/manual/make.html
to learn more about `make`.


