.. admonition:: GitHub-only

    WARNING: If you are reading this on GitHub, DON'T! Read the documentation at `api.plone.org <http://api.plone.org/contribute/develop.html>`_     so you have working references and proper formatting.


=======================
Development environment
=======================

This section is meant for contributors to the `plone.api` project.
Its purpose is to guide them through the steps needed to start contributing.

.. note ::: This HowTo is written for Linux and OS X users.
   If you're are running Windows we suggest using VMWare or a similar Virtualization tool to install Ubuntu Linux on a virtual machine or installing Ubuntu Linux as a secondary OS on your machine.
   Alternatively, you can browse Plone's documentation on how to get Plone development environment up and running on Windows.
   Plone does run on Windows but it's not completely trivial to set it up.


Locations of information and tools
==================================

* `Documentation @ api.plone.org <http://api.plone.org>`_
* `Source code @ GitHub <http://github.com/plone/plone.api>`_
* `Issues @ GitHub <http://github.com/plone/plone.api/issues>`_
* `Continuous Integration @ Travis CI <http://travis-ci.org/plone/plone.api>`_
* `Code Coverage @ Coveralls.io <http://coveralls.io/r/plone/plone.api>`_


Prerequisites
=============

System libraries
----------------

First let's look at 'system' libraries and applications that are normally installed with your OS packet manager, such as apt, aptitude, yum, etc.:

* ``libxml2`` - An xml parser written in C.
* ``libxslt`` - XSLT library written in C.
* ``git`` - Version control system.
* ``gcc`` - The GNU Compiler Collection.
* ``g++`` - The C++ extensions for gcc.
* ``GNU make`` - The fundamental build-control tool.
* ``GNU tar`` - The (un)archiving tool for extracting downloaded archives.
* ``bzip2`` and ``gzip`` decompression packages - ``gzip`` is nearly standard, however some platforms will require that ``bzip2`` be installed.
* ``Python 2.7`` - Linux distributions normally already have it, OS X users should use https://github.com/collective/buildout.python to get a clean Python version (the one that comes with OS X is broken).


Python tools
------------

Then you'll also need to install some Python specific tools:

* easy_install - the Python packaging system (download http://peak.telecommunity.com/dist/ez_setup.py and run ``sudo python2.7 ez_setup.py``.
* virtualenv - a tool that assists in creating isolated Python working environments. Run ``sudo easy_install virtualenv`` after your have installed   `easy_install` above.

.. note::

    Again, OS X users should use https://github.com/collective/buildout.python,
    it will make your life much easier to have a cleanly compiled Python instead of using the system one that is broken in many deeply confusing ways.


Further information
-------------------

If you experience problems read through the following links as almost all of the above steps are required for a default Plone development environment:

* http://plone.org/documentation/tutorial/buildout
* http://pypi.python.org/pypi/zc.buildout/
* http://pypi.python.org/pypi/setuptools
* http://plone.org/documentation/manual/installing-plone

If you are an OS X user, you first need a working Python implementation
(the one that comes with the operating system is broken).
Use https://github.com/collective/buildout.python and be happy.
Also applicable to other OSes, if getting a working Python proves a challenge.


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

Go make some tea while

* `make` creates an isolated Python environment in your `plone.api`` folder,
* bootstraps `zc.buildout`,
* fetches all dependencies,
* builds Plone,
* runs all tests and
* generates documentation so you can open it locally later on.

Other commands that you may want to run:

.. sourcecode:: bash

    [you@local plone.api]$ make tests  # run all tests and syntax validation
    [you@local plone.api]$ make docs   # re-generate documentation
    [you@local plone.api]$ make clean  # reset your env back to a fresh start
    [you@local plone.api]$ make        # re-build env, generate docs, run tests

Open ``Makefile`` in your favorite code editor to see all possible commands and what they do.
And read http://www.gnu.org/software/make/manual/make.html to learn more about `make`.


.. _working-on-an-issue:

Working on an issue
===================

Our GitHub account contains a `list of open issues <https://github.com/plone/plone.api/issues>`_.
Click on one that catches your attention.
If the issue description says ``No one is assigned`` it means no-one is already working on it and you can claim it as your own.
Click on the button next to the text and make yourself the one assigned for this issue.

Based on our :ref:`git_workflow` all new features must be developed in separate git branches.
So if you are not doing a very trivial fix, but rather adding new features/enhancements, you should create a *feature branch*.
This way your work is kept in an isolated place where you can receive feedback on it, improve it, etc.
Once we are happy with your implementation, your branch gets merged into *master* at which point everyone else starts using your code.

.. sourcecode:: bash

    [you@local plone.api]$ git checkout master  # go to master branch
    [you@local plone.api]$ git checkout -b issue_17  # create a feature branch
    # replace 17 with the issue number you are working on

    # change code here

    [you@local plone.api]$ git add -p && git commit  # commit my changes
    [you@local plone.api]$ git push origin issue_17  # push my branch to GitHub
    # at this point others can see your changes but they don't get effected by
    them; in other words, others can comment on your code without your code
    changing their development environments

Read more about Git branching at http://learn.github.com/p/branching.html.
Also, to make your git nicer, read the :ref:`setting_up_git` chapter.


Once you are done with your work and you would like us to merge your changes into master, go to GitHub to do a *pull request*.
Open a browser and point it to ``https://github.com/plone/plone.api/tree/issue_<ISSUE_NUMBER>``.
There you should see a ``Pull Request`` button.
Click on it, write some text about what you did and anything else you would like to tell the one who will review your work, and finally click ``Send pull request``.
Now wait that someone comes by and merges your branch (don't do it yourself, even if you have permissions to do so).

An example pull request text::

    Please merge my branch that resolves issue #13,
    where I added the get_navigation_root() method.


Commit checklist
================

Before every commit you should:

* Run unit tests and syntax validation checks.
* Add an entry to :ref:`changes` (if applicable).
* Add/modify :ref:`sphinx-docs` (if applicable).

All syntax checks and all tests can be run with a single command.
This command also re-generates your documentation.

.. sourcecode:: bash

    $ make

.. note::
    It pays off to invest a little time to make your editor run `pep8` and `pyflakes` on a file every time you save that file
    (or use `flake8` which combines both).
    This saves you lots of time in the long run.

