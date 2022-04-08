# Development environment

This section is meant for contributors to the `plone.api` project.
Its purpose is to guide them through the steps needed to start contributing.

% note ``` This HowTo is written for Linux and OS X users.
% If you're are running Windows we suggest using VMWare or a similar Virtualization tool to install Ubuntu Linux on a virtual machine or installing Ubuntu Linux as a secondary OS on your machine.
% Alternatively, you can browse Plone's documentation on how to get Plone development environment up and running on Windows.
% Plone does run on Windows but it's not completely trivial to set it up.

## Locations of information and tools

- [Documentation @ docs.plone.org](https://docs.plone.org)
- [Source code @ GitHub](https://github.com/plone/plone.api)
- [Issues @ GitHub](https://github.com/plone/plone.api/issues)
- [Code Coverage @ Coveralls.io](https://coveralls.io/github/plone/plone.api)

## Prerequisites

### System libraries

First let's look at 'system' libraries and applications that are normally installed with your OS packet manager, such as apt, aptitude, yum, etc.:

- `libxml2` - An xml parser written in C.
- `libxslt` - XSLT library written in C.
- `git` - Version control system.
- `gcc` - The GNU Compiler Collection.
- `g++` - The C++ extensions for gcc.
- `GNU make` - The fundamental build-control tool.
- `GNU tar` - The (un)archiving tool for extracting downloaded archives.
- `bzip2` and `gzip` decompression packages - `gzip` is nearly standard, however some platforms will require that `bzip2` be installed.
- `Python 2.7` - Linux distributions normally already have it, OS X users should use <https://github.com/collective/buildout.python> to get a clean Python version (the one that comes with OS X is broken).

### Python tools

- tox automation - tox aims to automate and standardize testing in Python. It is part of a larger vision of easing the packaging, testing and release process of Python software. Install with `pip install tox`.

```{note}
Again, OS X users should use <https://github.com/collective/buildout.python>,
it will make your life much easier to have a cleanly compiled Python instead of using the system one that is broken in many deeply confusing ways.
```

### Further information

If you experience problems read through the following links as almost all of the above steps are required for a default Plone development environment:

- <https://docs.plone.org/manage/index.html>
- <https://pypi.org/project/zc.buildout/>
- <https://pypi.org/project/setuptools/>
- <https://plone.org/download>

If you are an OS X user, you first need a working Python implementation
(the one that comes with the operating system is broken).
Use <https://github.com/collective/buildout.python> and be happy.
Also applicable to other OSes, if getting a working Python proves a challenge.

(git-workflow)=

## Git workflow & branching model

Our repository on GitHub has the following layout:

- **feature branches**: all development for new features must be done in
  dedicated branches, normally one branch per feature,
- **master branch**: when features get completed they are merged into the
  master branch; bugfixes are commited directly on the master branch,
- **tags**: whenever we create a new release we tag the repository so we can
  later re-trace our steps, re-release versions, etc.

### Squashing commits

In order to keep a clear and concise git history, it is good practice to squash commits before merging.
Use `git rebase --interactive` to squash all commits that you think are unnecessary.

## Creating and using the development environment

```{eval-rst}
.. todo::

    Update this section as it seams out of date, there is no Makefile so this description makes no sense anymore.
```

Go to your projects folder and download the lastest `plone.api` code:

```shell
cd <your_work_folder>
git clone https://github.com/plone/plone.api.git
```

Now `cd` into the newly created directory and build your environment:

```shell
cd plone.api
make
```

Go make some tea while

- `make` creates an isolated Python environment in your `` plone.api` `` folder,
- bootstraps `zc.buildout`,
- fetches all dependencies,
- builds Plone,
- runs all tests and
- generates documentation so you can open it locally later on.

Other commands that you may want to run:

```shell
make tests  # run all tests and syntax validation
make docs   # re-generate documentation
make clean  # reset your env back to a fresh start
make        # re-build env, generate docs, run tests
```

Open `Makefile` in your favorite code editor to see all possible commands and what they do.
And read <http://www.gnu.org/software/make/manual/make.html> to learn more about `make`.

(working-on-an-issue)=

## Working on an issue

Our GitHub account contains a [list of open issues](https://github.com/plone/plone.api/issues).
Click on one that catches your attention.
If the issue description says `No one is assigned` it means no-one is already working on it and you can claim it as your own.
Click on the button next to the text and make yourself the one assigned for this issue.

Based on our {ref}`git-workflow` all new features must be developed in separate git branches.
So if you are not doing a very trivial fix, but rather adding new features/enhancements, you should create a *feature branch*.
This way your work is kept in an isolated place where you can receive feedback on it, improve it, etc.
Once we are happy with your implementation, your branch gets merged into *master* at which point everyone else starts using your code.

```shell
git checkout master  # go to master branch
git checkout -b issue_17  # create a feature branch
# replace 17 with the issue number you are working on

# change code here

git add -p && git commit  # commit my changes
git push origin issue_17  # push my branch to GitHub
```

At this point, others can see your changes, but they don't get affected by them.
In other words, others can comment on your code without your code changing their development environments.

Read more about Git branching at <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches> and on our Git workflow at [Working with Git and GitHub](https://docs.plone.org/develop/coredev/docs/git.html).

Once you are done with your work and you would like us to merge your changes into master, go to GitHub to do a *pull request*.
Open a browser and point it to `https://github.com/plone/plone.api/tree/issue_<ISSUE_NUMBER>`.
There you should see a `Pull Request` button.
Click on it, write some text about what you did and anything else you would like to tell the one who will review your work, and finally click `Send pull request`.
Now wait that someone comes by and merges your branch (don't do it yourself, even if you have permissions to do so).

An example pull request text:

```
Please merge my branch that resolves issue #13,
where I added the get_navigation_root() method.
```

## Commit checklist

Before every commit you should:

- Run unit tests and syntax validation checks.
- Add an entry to `CHANGES.rst` (if applicable).

All syntax checks and all tests can be run with a single command.
This command also re-generates your documentation.

```shell
make
```

```{note}
It pays off to invest a little time to make your editor run `pep8` and `pyflakes` on a file every time you save that file
(or use `flake8` which combines both).
This saves you lots of time in the long run.
```

## Travis Continuous Integration

On every push to GitHub, [Travis](https://travis-ci.org/plone/plone.api) runs all tests and syntax validation checks and reports build outcome to the `#sprint` IRC channel and the person who committed the last change.

Travis is configured with the `.travis.yml` file located in the root of this package.

## Sphinx Documentation

```{note}
Un-documented code is broken code.
```

For every feature you add to the codebase, you should also add documentation for it to `docs/`.

After adding or modifying documentation, run `tox -e plone6docs` to re-generate your documentation.

Publicly available documentation on [6.dev-docs.plone.org/plone.api](https://6.dev-docs.plone.org/plone.api) is automatically generated from these source files, periodically.
So when you push changes to master on GitHub you should soon be able to see them published on [6.dev-docs.plone.org/plone.api](https://6.dev-docs.plone.org/plone.api).

Read the [General Guide to Writing Documentation](https://6.dev-docs.plone.org/contributing/writing-docs-guide.html) to brush up on your `MyST` skills.

Example:

```python
def add(a, b):
    """Calculate the sum of the two parameters.

    Also see the :func:`mod.path.my_func`, :meth:`mod.path.MyClass.method` and :attr:`mod.path.MY_CONSTANT` for more details.

    :param a: The first operand.
    :type a: :class:`mod.path.A`

    :param b: The second operand.
    :type b: :class:`mod.path.B`

    :rtype: int
    :return: The sum of the operands.
    :raises: `KeyError`, if the operands are not the correct type.
    """
```

Attributes are documented using the `#:` marker above the attribute.
The documentation may span multiple lines.

```python
#: Description of the constant value
MY_CONSTANT = 0xc0ffee

class Foobar(object):

    #: Description of the class variable which spans over
    #: multiple lines
    FOO = 1
```
