(releasing-a-new-version)=

# Releasing a new version

Releasing a new version of `plone.api` involves the following steps:

1. Prepare source for a new release.
2. Create a git tag for the release.
3. Push the git tag upstream to GitHub.
4. Generate a distribution file for the package.
5. Upload the generated package to Python Package Index (PyPI).

To avoid human errors and to automate some of the tasks above we use `jarn.mkrelease`.
It's listed as a dependency in `setup.py` and should already be installed in your local bin:

```shell
bin/mkrelease --help
```

Apart from that, in order to be able to upload a new version to PyPI you need to be listed under `Package Index Owner` list and you need to configure your PyPI credentials in the `~/.pypirc` file, e.g.:

```
[distutils]
index-servers =
  pypi

[pypi]
username = fred
password = secret
```

## Checklist

Follow these step to create a new release of `plone.api`.

1. Verify that we have documented all changes in the `CHANGES.rst` file.
   Go through the list of commits since last release on GitHub and check all changes are documented.
2. Modify the version identifier in the `setup.py` to reflect the version of the new release.
3. Confirm that the package description (generated from `README.md` and others) renders correctly by running `bin/longtest` and open its output in your favorite browser.
4. Commit all changes to the git repository and push them upstream to GitHub.
5. Create a release, tag it in git and upload it to GitHub by running `bin/mkrelease -d pypi -pq .` (see example below).

## Example

In the following example we are releasing version 0.1 of `plone.api`.
The package has been prepared so that `setup.py` contains the version `0.1`,
this change has been committed to git and all changes have been pushed upstream to GitHub:

```shell
# Check that package description is rendered correctly
bin/longtest

# Make a release and upload it to PyPI
bin/mkrelease -d pypi -pq ./
```
```console
Releasing plone.api 0.1
Tagging plone.api 0.1
To git@github.com:plone/plone.api.git
* [new tag]         0.1 -> 0.1
running egg_info
running sdist
warning: sdist: standard file not found: should have one of README, README.txt
running register
Server response (200): OK
running upload
warning: sdist: standard file not found: should have one of README, README.txt
Server response (200): OK
done
```

```{note}
Please ignore the sdist warning about README file above.
PyPI does not depend on it and it's just a bug in setupools (reported and waiting to be fixed).
```
