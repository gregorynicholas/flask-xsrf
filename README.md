flask_xsrf
==========

[flask](http://flask.pocoo.org) extension for defending against cross-site
request forgery attacks (xsrf/csrf)


<br>
**build-status:**

`master ` [![travis-ci build-status: master](https://secure.travis-ci.org/gregorynicholas/flask-xsrf.svg?branch=master)](https://travis-ci.org/gregorynicholas/flask-xsrf)
<br>
`develop` [![travis-ci build-status: develop](https://secure.travis-ci.org/gregorynicholas/flask-xsrf.svg?branch=develop)](https://travis-ci.org/gregorynicholas/flask-xsrf)


**links:**

* [homepage](http://gregorynicholas.github.io/flask-xsrf)
* [source](http://github.com/gregorynicholas/flask-xsrf)
* [python-package](http://packages.python.org/flask-xsrf)
* [github-issues](https://github.com/gregorynicholas/flask-xsrf/issues)
* [changelog](https://github.com/gregorynicholas/flask-xsrf/blob/master/CHANGES.md)
* [travis-ci](http://travis-ci.org/gregorynicholas/flask-xsrf)


<br>
-----
<br>


### getting started


install with pip:

    $ pip install flask-xsrf


<br>
-----
<br>


### features

* [todo]


<br>
-----
<br>


### example usage

    from flask import Flask, Response, session
    app = Flask(__name__)
    app.debug = True
    app.secret_key = 'session_secret_key'
    app.config['session_cookie_secure'] = True
    app.config['remember_cookie_name'] = 'testdomain.com'
    app.config['remember_cookie_duration_in_days'] = 1

    @app.before_request
    def before_request():
      if 'user_id' not in session:
        session['user_id'] = 'random_generated_anonymous_id'

    def get_user_id():
      return session.get('user_id')

    xsrfh = xsrf.XSRFTokenHandler(
      user_func=get_user_id, secret='xsrf_secret', timeout=3600)

    @app.route('/test', methods=['GET'])
    @xsrfh.send_token()
    def test_get():
      return Response('success')

    @app.route('/test', methods=['POST'])
    @xsrfh.handle_token()
    def test_post():
      return Response('success')
