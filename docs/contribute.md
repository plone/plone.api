---
myst:
  html_meta:
    "description": "Contribute to plone.api"
    "property=og:description": "Contribute to plone.api"
    "property=og:title": "Contribute to plone.api"
    "keywords": "plone.api, contribute, Plone, API, development"
---

# Contribute to `plone.api`

This section describes how to contribute to the `plone.api` project.
It extends {doc}`plone:contributing/index`.

## Prerequisites

Prepare your system by installing prerequisites.

### System libraries

You need to install system libraries, as described in {ref}`plone:plone-prerequisites-label`.


## Create development environment

After satisfying the prerequisites, you are ready to create your development environment.
`plone.api` uses `tox` as a wrapper around `coredev.buildout` to simplify development, whereas Plone core uses `coredev.buildout` directly.
Additionally `plone.api` uses `make` commands that invoke the `tox` commands as a convenience and for consistency across Plone packages.

Start by changing your working directory to your project folder, and check out the latest `plone.api` source code.

```shell
cd <your_project_folder>
git clone https://github.com/plone/plone.api.git
```

Run `make help` to see the available `make` commands.

```console
check                          Check code base according to Plone standards
clean                          Clean environment
help                           This help message
linkcheck                      Check links in documentation
livehtml                       Build docs and watch for changes
test                           Run tests
```

The `make` commands `check`, `livehtml`, and `test` will create a development environment, if it does not already exist.

Test your code changes with the following command.

```shell
make test
```


(git-workflow)=

## git

Use the following git branches when contributing to `plone.api`.

feature branches
: All development for a new feature or bug fix must be done on a new branch.

`main`
: Pull requests should be made from a feature branch against the `main` branch.
When features and bug fixes are complete and approved, they are merged into the `main` branch.

```{seealso}
{ref}`plone:contributing-core-work-with-git-label`
```

## Continuous integration

`plone.api` uses GitHub workflows for continuous integration.
On every push to the `main` branch, GitHub runs its workflows for all tests and code quality checks.
GitHub workflows are configured in the directory `.github/workflows` at the root of this package.

## Documentation

For every feature change or addition to `plone.api`, you must add documentation of it.
`plone.api` uses [MyST](https://myst-parser.readthedocs.io/en/latest/) for documentation syntax.

```{seealso}
{doc}`plone:contributing/documentation/index`
```

When adding or modifying documentation, you can build the documentation with the following command.
As you edit the documentation, the started process automatically reloads your changes in the web browser.

```shell
make livehtml
```

You can run a link checker on documentation.

```shell
make linkcheck
```

The [`plone.api` documentation](https://6.docs.plone.org/plone.api) is automatically generated from the documentation source files when its submodule is updated in the [main Plone `documentation` repository](https://github.com/plone/documentation/).

## Add a function to an existing module

This section describes how to add a new function `foo` to `plone.api`.

The function would go in the module `plone.api.content`, located in the file {file}`src/plone/api/content.py`.

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
% InvalidParameterError,
% lambda: foo("/plone/blog", "abcd001")
% )
%
% # Make it available for testing below
% from plone import api
% api.content.foo = foo

Add documentation in {file}`docs/api/content.md`.
Narrative documentation should describe what your function does.

You should also write some tests in code blocks.
`TestCase` methods, such as `self.assertEqual()`, are available in `doctests`.
See [unittest.TestCase assert methods](https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug) for all available methods.
The file is linked in `/src/plone/api/tests/doctests/`, which includes the doctests in `plone.api`'s test setup.
The package `manuel` allows you to write doctests as common Python code in code blocks.

The following example shows narrative documentation and doctests.

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
% self.assertEqual(blog_foo, "foo")

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
% self.assertEqual(blog_foo, "foo")
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
The function references the narrative documentation via the label `content-foo-example`.
The narrative documentation references the API function documentation via `` {meth}`api.content.foo` ``.
The documentation is rendered with a link from the API reference to the narrative documentation, which in turn links back to the API reference.

## Resources

- {doc}`plone:index`
- [Source code](https://github.com/plone/plone.api)
- [Issue tracker](https://github.com/plone/plone.api/issues)
