#!/usr/bin/env python
"""
flask-xsrf
~~~~~~~~~~

a flask extension for defending against cross-site request forgery attacks
(xsrf/csrf).


links
`````

* `docs <http://gregorynicholas.github.io/flask-xsrf>`_
* `source <http://github.com/gregorynicholas/flask-xsrf>`_
* `package <http://packages.python.org/flask-xsrf>`_
* `travis-ci <http://travis-ci.org/gregorynicholas/flask-xsrf>`_

"""
from setuptools import setup

__version__ = "1.0.2"

with open("requirements.txt", "r") as f:
  requires = f.readlines()

with open("README.md", "r") as f:
  long_description = f.readlines()


setup(
  name='flask-xsrf',
  version=__version__,
  url='http://github.com/gregorynicholas/flask-xsrf',
  license='MIT',
  author='gregorynicholas',
  author_email='gn@gregorynicholas.com',
  description=__doc__,
  long_description=long_description,
  zip_safe=False,
  platforms='any',
  install_requires=requires,
  py_modules=[
    'flask_xsrf',
    'flask_xsrf_tests',
  ],
  dependency_links=[
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development :: Libraries :: Python Modules'
  ]
)
