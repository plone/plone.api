---
myst:
  html_meta:
    "description": "How to set up your develoment environment to contribute"
    "property=og:description": "How to set up your develoment environment to contribute"
    "property=og:title": "Development environment"
    "keywords": "contribute, Plone, API, development"
---

# Development environment

{sub-ref}`today`

This section is meant for contributors to the `plone.api` project.
Its purpose is to guide them through the steps needed to start contributing.

```{note}
This HowTo is written for Linux and OS X users.
If you are running Windows, we suggest using either Windows Subsystem for Linux, VMWare or a similar virtualization tool to install Ubuntu Linux on a virtual machine, or installing Ubuntu Linux as a secondary operating system on your machine.
Alternatively, you can browse Plone's documentation on how to get Plone development environment up and running on Windows.
Plone does run on Windows, but it's not completely trivial to set it up.
```

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
- `GNU tar` - The (un)archiving tool for extracting downloaded archives.
- `bzip2` and `gzip` decompression packages - `gzip` is nearly standard, however some platforms will require that `bzip2` be installed.
- `Python 3` - It is recommended to use a Python virtual environment, using tools such as pyenv or venv, to get a clean Python version.

### Python tools

tox automation
: `tox` aims to automate and standardize testing in Python.
  It is part of a larger vision of easing the packaging, testing, and release process of Python software.
  Install with `pip install tox`.


### Further information

If you experience problems, read through the following links as almost all of the above steps are required for a default Plone development environment:

- <https://docs.plone.org/manage/index.html>
- <https://pypi.org/project/zc.buildout/>
- <https://pypi.org/project/setuptools/>
- <https://plone.org/download>


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

Go to your projects folder and download the lastest `plone.api` code:

```shell
cd <your_work_folder>
git clone https://github.com/plone/plone.api.git
```

Now `cd` into the newly created directory and build your environment:

```shell
cd plone.api
pip install tox
tox
```

Go make some tea while `tox` runs all tasks listed under `tox -l`.

- runs all checks and tests
- generates documentation so you can open it locally later on

Other commands that you may want to run:

```shell
tox -e py39-plone-60  # run all tests for Python 3.9 and Plone 6
tox -e plone6docs     # re-generate documentation
```

Run `tox -l` to list all tox environments.
Open `tox.ini` in your favorite code editor to see all possible commands and what they do.
Read <https://tox.wiki/en/latest/> to learn more about `tox`.


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
git checkout master       # go to master branch
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
- Add an entry to `/news/` (if applicable).

All syntax checks and all tests can be run with a single command.
This command also re-generates your documentation.

```shell
tox
```

```{note}
It pays off to invest a little time to make your editor run `pep8` and `pyflakes` on a file every time you save that file
(or use `flake8` which combines both).
This saves you lots of time in the long run.
```


## GitHub Continuous Integration

On every push GitHub runs all tests and syntax validation checks.
GitHub CI is configured in `.github/workflow` in the root of this package.


## Sphinx Documentation

```{note}
Un-documented code is broken code.
```

For every feature you add to the codebase, you should also add documentation of it to `docs/`.

After adding or modifying documentation, run `tox -e plone6docs` to re-generate your documentation.

Publicly available documentation on [6.docs.plone.org/plone.api](https://6.docs.plone.org/plone.api) is automatically generated from these source files when its submodule is updated in the [main Plone `documentation` repository](https://github.com/plone/documentation/).

For writing narrative documentation, read the [General Guide to Writing Documentation](https://6.docs.plone.org/contributing/writing-docs-guide.html).

### Adding a function to an existing module

Example: Add a new function `plone.api.content.foo`.

The function would go in the module `plone.api.content`.
Therefore you would add your function in `/src/plone/api/content.py`.

% invisible-code-block: python
%
% from plone.api.validation import at_least_one_of
% from plone.api.validation import mutually_exclusive_parameters

```python
@mutually_exclusive_parameters('path', 'UID')
@at_least_one_of('path', 'UID')
def foo(path=None, UID=None):
    """Do foo.

    :param path: Path to the object we want to get,
        relative to the portal root.
    :type path: string

    :param UID: UID of the object we want to get.
    :type UID: string

    :returns: String
    :raises:
        :class:`~plone.api.exc.MissingParameterError`,
        :class:`~plone.api.exc.InvalidParameterError`
    :Example: :ref:`content-foo-example`
    """
    return "foo"
```

% invisible-code-block: python
%
% bar = foo('/plone/blog')
% self.assertEqual(bar,"foo")
%
% from plone.api.exc import InvalidParameterError
% self.assertRaises(
%     InvalidParameterError,
%     lambda: foo("/plone/blog", "abcd001")
% )

Add documentation in `/docs/content.md`.
Describe what your function does, and write some tests in code blocks.
`TestCase` methods such as `self.assertEqual()` are available in `doctests`.
See [unittest.TestCase assert methods](https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug) for all available methods.
The file is linked in `/src/plone/api/tests/doctests/`, which includes the doctests in `plone.api` testing set up.
The package `manuel` allows you to write doctests as common Python code in code blocks.

````markdown
(content-foo-example)=

## Get the foo of an object

You can use the {meth}`api.content.foo` function to get the `foo` of an object.

```python
from plone import api
blog_foo = api.content.foo(path="/plone/blog")
```

% invisible-code-block: python
%
% self.assertEqual(blog_foo,"foo")
````

Code blocks are rendered in documentation.

````markdown
```python
from plone import api
blog_foo = api.content.foo(path="/plone/blog")
```
````

Invisible code blocks are not rendered in documentation and can be used for tests.

```markdown
% invisible-code-block: python
%
% self.assertEqual(blog_foo,"foo")
```

Invisible code blocks are also handy for enriching the namespace without cluttering the narrative documentation.

```markdown
% invisible-code-block: python
%
% portal = api.portal.get()
% image = api.content.create(type='Image', id='image', container=portal)
% blog = api.content.create(type='Link', id='blog', container=portal)
```

Functions and examples in documentation are mutually referenced.
The function references the narrative documentation via label `content-foo-example`.
The narrative documentation references the API function documentation via `` {meth}`api.content.foo` ``.
The documentation is rendered with a link from the API reference to the narrative documentation, which in turn links back to the API reference.
