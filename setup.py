#!/usr/bin/env python
"""
flask_xsrf
--------------

A Flask extension for defending against cross-site request forgery attacks
(XSRF/CSRF).

http://github.com/gregorynicholas/flask-xsrf
`````

* `documentation <http://packages.python.org/flask_xsrf>`_
* `development version
  <http://github.com/gregorynicholas/flask-xsrf/zipball/master#egg=flask_xsrf-dev>`_

"""
from setuptools import setup

setup(
  name='flask-xsrf',
  version='1.0.1',
  url='http://github.com/gregorynicholas/flask-xsrf',
  license='MIT',
  author='gregorynicholas',
  description='A Flask extension for XSRF/CSRF protection.',
  long_description=__doc__,
  packages=[
  ],
  namespace_packages=[
  ],
  py_modules=[
    'flask_xsrf',
  ],
  zip_safe=False,
  platforms='any',
  install_requires=[
    'flask==0.9',
    'werkzeug==0.8.3',
    'blinker==1.2',
  ],
  dependency_links = [
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
