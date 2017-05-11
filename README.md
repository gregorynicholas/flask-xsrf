# flask-xsrf

[flask](http://flask.pocoo.org) extension for defending against *cross-site request forgery attacks*
[(xsrf/csrf)](https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)),
by protecting flask request endpoints with uniquely generated tokens for each
request.




<div style="text-align:center">
  <img title="flask-xsrf" src="https://cloud.githubusercontent.com/assets/407650/15816952/574714be-2b8a-11e6-801f-8aacc0a73620.png">
</div>


<br>
<br>



| FLASK | PYTHON | XSRF |
| ----- | ------ | ---- |
| [![flask](https://cloud.githubusercontent.com/assets/407650/15803510/2d4f594a-2a96-11e6-86e0-802592e17aca.png)](http://flask.pocoo.org) | [![python](https://cloud.githubusercontent.com/assets/407650/15803508/24d88944-2a96-11e6-9912-c696d9fc3912.png)](http://www.python.org) | [![csrf](https://cloud.githubusercontent.com/assets/407650/15803506/1c76e002-2a96-11e6-881e-969ef407839a.png)](https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)) |

<br>
<br>


-----
<br>
<br>



**BUILD STATUS**

| branch   | service       | status                           | service | title           | status                 |
| -------  | ------------  | -------------------------------- | ------- | --------------- | ---------------------- |
| `master` | `ci-build` | [![travis-ci-build-status-master](https://secure.travis-ci.org/gregorynicholas/flask-xsrf.svg?branch=master)](https://travis-ci.org/gregorynicholas/flask-xsrf/builds) | `github` | `tags` | [![github-tags](https://img.shields.io/github/tag/gregorynicholas/flask-xsrf.svg?maxAge=2592000?style=flat-square)](https://github.com/gregorynicholas/flask-xsrf/tags) |
| `develop` | `ci-build` | [![travis-ci-build-status-develop](https://secure.travis-ci.org/gregorynicholas/flask-xsrf.svg?branch=develop)](https://travis-ci.org/gregorynicholas/flask-xsrf/builds) | `github` | `releases-all` | [![github-releases-all](https://img.shields.io/github/downloads/gregorynicholas/flask-xsrf/total.svg?maxAge=2592000?style=flat-square)](https://github.com/gregorynicholas/flask-xsrf/releases) |
| `master` | `coveralls.io` | [![coveralls-coverage-status-master](https://coveralls.io/repos/github/gregorynicholas/flask-xsrf/badge.svg?branch=master)](https://coveralls.io/github/gregorynicholas/flask-xsrf?branch=master) | `github` | `releases-latest` | [![github-releases-latest](https://img.shields.io/github/downloads/gregorynicholas/flask-xsrf/1.0.2/total.svg?maxAge=2592000?style=flat-square)](https://github.com/gregorynicholas/flask-xsrf/releases/latest) |
| `develop` | `coveralls.io` | [![coveralls-coverage-status-develop](https://coveralls.io/repos/github/gregorynicholas/flask-xsrf/badge.svg?branch=develop)](https://coveralls.io/github/gregorynicholas/flask-xsrf?branch=develop) | `pypi` | `releases-latest` | [![pypi-releases-latest](https://img.shields.io/pypi/v/flask-xsrf.svg)](https://pypi.python.org/pypi/flask-xsrf) |
| `master` | `landscape.io` | [![landscape-code-health-master](https://landscape.io/github/gregorynicholas/flask-xsrf/master/landscape.svg?style=flat-square)](https://landscape.io/github/gregorynicholas/flask-xsrf/master) | `pypi` | `downloads` | [![pypi-downloads](https://img.shields.io/pypi/dm/flask-xsrf.svg)](https://pypi.python.org/pypi/flask-xsrf) |
| `develop` | `landscape.io` | [![landscape-code-health-develop](https://landscape.io/github/gregorynicholas/flask-xsrf/develop/landscape.svg?style=flat-square)](https://landscape.io/github/gregorynicholas/flask-xsrf/develop) | `pypi` | `dl-month` | [![pypi](https://img.shields.io/pypi/dm/flask-xsrf.svg?maxAge=2592000?style=flat-square)](https://github.com/gregorynicholas/flask-xsrf) |



-----
<br>
<br>



**REFERENCE / LINKS**

* [pypi: package](http://packages.python.org/flask-xsrf)
* [readthedocs: docs](https://readthedocs.org/projects/flask-xsrf/)
* [github: wiki](https://github.com/gregorynicholas/flask-xsrf/wiki)
* [github: source](http://github.com/gregorynicholas/flask-xsrf)
* [github: releases](https://github.com/gregorynicholas/flask-xsrf/releases)
* [changelog notes](https://github.com/gregorynicholas/flask-xsrf/blob/master/CHANGES.md)
* [travis-ci: build-status](http://travis-ci.org/gregorynicholas/flask-xsrf)
* [coveralls: coverage-status](https://coveralls.io/github/gregorynicholas/flask-xsrf)
* [contributing notes](http://github.com/gregorynicholas/flask-xsrf/wiki)
* [github: issues](https://github.com/gregorynicholas/flask-xsrf/issues)




-----
<br>




### HOW IT WORKS

* flask route handlers are decorated to generate, send a uniquely hashed token
    * the hashed values are stored on the server, using flask sessions
    * the token is sent in the response header `X-XSRF-Token`
* on subsequent client requests..
    * the client will be expected to send the token back to the server
      * either through form data, or through the header `X-XSRF-Token`
    * to the server receive, validate uniquely hashed tokens

![diagram of an xsrf attack](https://cloud.githubusercontent.com/assets/407650/15803515/4ec0a606-2a96-11e6-891c-378f52e6f82b.jpg)


**FEATURES**

* **flexible** - decide which style of implementation suits you best.
    * capture, validate `XSRF-Tokens` through headers, cookies, form-fields; the style is an easily configurable choice.
* **timeout** - optionally, you can specify a default time window for valid tokens
* **tested** - used internally @ google.




-----
<br>




### USAGE


**REQUIREMENTS**

| python   | flask     |
| ------   | -----     |
| `2.7.6+` | `0.11.0+` |


<br>
<br>


**INSTALLATION**

install with pip _(more often it is recommended to lock / specify a specific version)_:

```sh
pip install --disable-pip-version-check flask-xsrf
pip install --disable-pip-version-check flask-xsrf==1.0.3
```


**IMPLEMENTATION**

implementation of the library with your flask app breaks down into four steps.

1: add a `secret_key` to your flask app config object:

```py
from flask import Flask

flask_app = Flask(__name__)
flask_app.secret_key = '<:session_secret_key>'
flask_app.config['session_cookie_secure'] = True
flask_app.config['remember_cookie_name'] = 'testdomain.com'
flask_app.config['remember_cookie_duration_in_days'] = 1
```

2: create an instance of an `XSRFTokenHandler` object, and specify a method/callable
which will be used as a getter by the token handler to get a `user_id`.
optionally, you can assign auto-generated id's for anonymous requests.
lastly, you may specify a default `timeout`, in number of seconds, to expire
tokens after a specific the amount of time:

```py
from flask import Response
from flask import session
import flask_xsrf as xsrf

@flask_app.before_request
def before_request():
  if 'user_id' not in session:
    session['user_id'] = 'random_generated_anonymous_id'

def get_user_id():
  return session.get('user_id')

xsrf_handler = xsrf.XSRFTokenHandler(
  user_fn=get_user_id, secret='xsrf_secret', timeout=3600)
```

_NOTE: currently, usage of the `session` is required ([see TODO notes below](#todos))._


3: decorate `GET` request-handlers to send a generated token:

```py
@flask_app.route('/test', methods=['GET'])
@xsrf_handler.send_token()
def test_get():
  return Response('success')
```


4: decorate `POST` request-handlers to receive, validate sent tokens:

```py
@flask_app.route('/test', methods=['POST'])
@xsrf_handler.handle_token()
def test_post():
  return Response('success')
```

<br>


##### TO SUMMARIZE

that's all there is to it. please feel free to contact me <gn@gregorynicholas.com>
or to [submit an issue on github](https://github.com/gregorynicholas/flask-xsrf/issues)
for any questions or help. however, creating a fork and submitting pull-requests
are much preferred. contributions will be very much appreciated.




-----
<br>




### CONTRIBUTING


**STAR, FORK THIS PROJECT**

| `forks` | `stars` |
| -------------- | -------------- |
| [![github forks](https://img.shields.io/github/forks/gregorynicholas/flask-xsrf.svg?style=social&label=Fork&maxAge=2592000?style=flat-square)](https://github.com/gregorynicholas/flask-xsrf/fork) | [![github stars](https://img.shields.io/github/stars/gregorynicholas/flask-xsrf.svg?style=social&label=Star&maxAge=2592000?style=flat-square)](https://github.com/gregorynicholas/flask-xsrf/stargazers) |



<br>


**LOCAL ENVIRONMENT SETUP (OSX)**

here's a list summary of the python environment setup:

* setup `pyenv`, `pyenv-python-2.7.11`
* setup `virtualenv`, `virtualenvwrapper`
    * create project `virtualenv`
    * with a command such as `$ mkvirtualenv flask-xsrf-dev`
* install pip dependencies
* install local development build
    * `$ python setup.py --verbose develop`


<br>


**INSTALL PYENV**

pyenv (aka NVM or RVM for python) allows installing python at specific versions,
and helps to manage multiple versions on osx. install is easy, and can be tricky
to work with, unless you remember to set the proper environment shell variables:
```sh
init-pyenv(){
  export PYENV_ROOT="$HOME/.pyenv"
  export PYENV_PY_VERSION="2.7.11"
  export PYENV_VERSION_BIN_DIR="$PYENV_ROOT/versions/$PYENV_PY_VERSION/bin"
  export PYENV_BUILD_ROOT="$PYENV_ROOT/sources"
  export PYENV_SHIMS_DIR="$PYENV_ROOT/shims"
  export PYENV_SHELL="bash"
  export PYENV_DEBUG=0
  export PATH="$PYENV_ROOT/bin:$PYENV_VERSION_BIN_DIR:$PATH"
}

init-virtualenv(){
  export VIRTUALENVWRAPPER_SCRIPT="$PYENV_VERSION_BIN_DIR/virtualenvwrapper.sh"
  export WORKON_HOME="$HOME/.virtualenvs"
  export PIP_VIRTUALENV_BASE=$
  . "$VIRTUALENVWRAPPER_SCRIPT"
}
```

now we're ready to install pyenv/python:
```sh
init-pyenv
git clone https://github.com/yyuu/pyenv.git "$PYENV_ROOT"
eval "$(pyenv init -)"
pyenv install 2.7.11 && say "pyenv install of python 2.7.11 complete"
pyenv rehash
pyenv global 2.7.11
```

next, configure virtualenv:
```sh
init-virtualenv
pyenv exec pip install --disable-pip-version-check --upgrade pip
pyenv exec pip install --disable-pip-version-check virtualenv && pyenv rehash
pyenv exec pip install --disable-pip-version-check virtualenvwrapper && pyenv rehash
```

next, create the project virtualenv, install dependencies:
```sh
mkvirtualenv flask-xsrf-dev && pyenv rehash
workon flask-xsrf-dev && pyenv rehash
pyenv exec pip install --disable-pip-version-check -r .serpent/runtime-config/pip/requirements.txt && pyenv rehash
```



<br>



**DEVELOPMENT FLOW**

* TODO: generate asciicinema movie clip of setup steps..?
* activate the environment
    * `$ init-pyenv`
    * `$ init-virtualenv`
    * `$ eval "$(pyenv init -)"`
    * `$ workon flask-xsrf-dev`
* run tests
    * `$ python setup.py nosetests`
* view coverage report
    * `$ coverage report --show-missing`

<br>

viola. that's pretty much all there is to the flow (for now..).


<br>


-----
<br>





#### TODOs

* add feature: enable checking of referer headers / client ip-address
* remove hard-coded dependency / usage of `session`.
* add feature: enable storage of tokens in cookie.
    * this might help ease implementation, as the client would not have to manually manage passing of tokens to server.


-----
<br>




#### COPYRIGHT, LICENSE

the derived work is distributed under the [Apache License Version 2.0](http://opensource.org/licenses/Apache-2.0).



<br>
