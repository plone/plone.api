"""Run doctests included in documentation as code blocks.

group.md

Create a group:

```python
from plone import api

group = api.group.create(
    groupname='board_members',
    title='Board members',
    description='Just a description',
    roles=['Reader', ],
    groups=['Site Administrators', ],
)
```

Test the group:

% invisible-code-block: python
%
% self.assertEqual(group.id, 'board_members')
% self.assertEqual(group.getProperty('title'), 'Board members')
% self.assertEqual(group.getProperty('description'), 'Just a description')
% self.assertTrue('Reader' in group.getRoles())
% self.assertTrue('Site Administrators' in group.getMemberIds())

"""

from plone.api.tests.base import INTEGRATION_TESTING
from plone.testing import layered
from plone.testing.zope import Browser
from sybil import Sybil
from sybil.integration.unittest import TestCase
from sybil.parsers.doctest import DocTestParser
from sybil.parsers.myst.codeblock import PythonCodeBlockParser
from unittest import TestSuite


def sybil_setup(namespace):
    """Shared test environment set-up, ran before every test."""
    print("*** sybil_setup")
    print("namespace", namespace)
    layer = INTEGRATION_TESTING
    app = namespace.get('app', layer['app'])
    if not namespace.get('app'):
        namespace.update(
            {
                'app': app,
                'portal': namespace.get('portal', layer['portal']),
                'request': namespace.get('request', layer['request']),
                'browser': Browser(app),
            },
        )


sb = Sybil(
    parsers=[
        DocTestParser(),
        PythonCodeBlockParser(),
    ],
    path='./doctests',
    # TODO Switch back to *.md
    # pattern='*.md',
    pattern='testdoc.md',
    setup=sybil_setup,
)


def _load_tests(loader=None, tests=None, pattern=None):
    suite = TestSuite()
    for path in sorted(sb.path.glob('**/*')):
        if path.is_file() and sb.should_parse(path):
            document = sb.parse(path)

            SybilTestCase = type(
                document.path,
                (TestCase,),
                dict(
                    sybil=sb,
                    namespace=document.namespace,
                ),
            )

            for example in document:
                stc = SybilTestCase(example)
                stc.namespace.update(
                    {
                        'self': stc,
                    },
                )
                suite.addTest(stc)
    layeredSuite = layered(
        suite,
        layer=INTEGRATION_TESTING,
    )
    return layeredSuite


load_tests = _load_tests
