from setuptools import setup, find_packages

version = '1.0a1'

setup(name='plone.api',
      version=version,
      description='A Plone API.',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      license='GPL version 2',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['plone'],
      include_package_data=True,
      platforms='Any',
      zip_safe=False,
      install_requires=[
        'setuptools',
        'Plone',  # this is needed so we can pull docstrings into Sphinx
      ],
      extras_require={
        'test': ['plone.app.testing', 'mock'],
      },
      classifiers=[
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
      ],
)
