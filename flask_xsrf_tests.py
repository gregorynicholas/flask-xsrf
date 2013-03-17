#!/usr/bin/env python
import base64
import unittest
from flask.testsuite import FlaskTestCase
import flask_xsrf as xsrf

class XSRFTokenTests(unittest.TestCase):

  def test_verify_timeout_elapse_raises(self):
    """Test that the time span between generation and verification raises if
    the time span is greater than the timeout arg."""
    token = xsrf.XSRFToken(
      user_id='user@example.com',
      secret='secret',
      current_time=1354160000)
    token_string = token.generate_token_string()
    token.verify_token_string(
      token_string,
      timeout=10,
      current_time=1354160010)
    self.assertRaises(xsrf.XSRFTokenExpiredException,
      token.verify_token_string,
      token_string,
      timeout=10,
      current_time=1354160011)

  def test_verify_no_action_value_raises(self):
    """ """
    token = xsrf.XSRFToken(
      user_id='user@example.com',
      secret='secret',
      current_time=1354160000)
    token_string = token.generate_token_string()
    token.verify_token_string(token_string)
    self.assertRaises(
      xsrf.XSRFTokenInvalid,
      token.verify_token_string,
      xsrf.XSRFToken(
        user_id='user@example.com',
        secret='differentsecret',
        current_time=1354160000).generate_token_string())
    self.assertRaises(
      xsrf.XSRFTokenInvalid,
      token.verify_token_string,
      xsrf.XSRFToken(
        user_id='user@example.com',
        secret='secret',
        current_time=1354160000).generate_token_string('action'))

  def test_verify_different_action_values_raises(self):
    token = xsrf.XSRFToken(
      user_id='user@example.com',
      secret='secret',
      current_time=1354160000)
    token_string = token.generate_token_string('action')
    token.verify_token_string(token_string, 'action')
    self.assertRaises(
      xsrf.XSRFTokenInvalid,
      token.verify_token_string,
      xsrf.XSRFToken(
        user_id='user@example.com',
        secret='differentsecret',
        current_time=1354160000).generate_token_string())

  def test_verify_substring_of_tokenstr_fails(self):
    """Tests that a substring of the correct token fails to verify."""
    token = xsrf.XSRFToken(
      user_id='user@example.com',
      secret='secret',
      current_time=1354160000)
    token_string = token.generate_token_string()
    test_token, test_time = base64.urlsafe_b64decode(token_string).split('|')
    test_string = base64.urlsafe_b64encode(
      '|'.join([test_token[:-1], test_time]))

    self.assertRaises(
      xsrf.XSRFTokenInvalid,
      token.verify_token_string,
      test_string)

  def test_verify_tokenstr_not_b64_raises(self):
    """Tests that a token string must be a valid base64 string."""
    token = xsrf.XSRFToken(
      user_id='user@example.com',
      secret='secret')
    self.assertRaises(
      xsrf.XSRFTokenMalformed,
      token.verify_token_string, 'FAKE_STR_NOT_B64')

  def test_verify_tokenstr_wo_delimiter_raises(self):
    """Tests that a token string must properly created from the digest maker."""
    token = xsrf.XSRFToken(
      user_id='user@example.com',
      secret='secret')
    self.assertRaises(
      xsrf.XSRFTokenMalformed,
      token.verify_token_string,
      base64.b64encode('FAKE_STR_NO_DELIMITER'))

  def test_verify_tokenstr_not_int_time_raises(self):
    """Tests that the time must be a correct datetime int value."""
    token = xsrf.XSRFToken(
      user_id='user@example.com',
      secret='secret')
    self.assertRaises(
      xsrf.XSRFTokenMalformed,
      token.verify_token_string,
      base64.b64encode('FAKE_STR|FAKE_TIME_NOTINT'))


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


@app.errorhandler(xsrf.XSRFTokenInvalid)
def xsrftokeninvalid():
  return Response(status=400)

@app.errorhandler(xsrf.XSRFTokenMalformed)
def xsrftokenmalformed():
  return Response(status=400)

@app.errorhandler(xsrf.XSRFTokenExpiredException)
def xsrftokenexpiredexception():
  return Response(status=400)

@app.errorhandler(xsrf.XSRFTokenUserIdInvalid)
def xsrftokenuseridinvalid():
  return Response(status=400)


class XSRFTokenHandlerTests(FlaskTestCase):
  def setUp(self):
    self.app = app.test_client()

  def test_app_request_works(self):
    test_get = self.app.get(
      '/test', data='', headers={})
    self.assertEquals(test_get.status_code, 200)
    # assert the token string header
    token_string = test_get.headers.get('X-XSRF-Token')
    self.assertTrue(token_string and len(token_string) > 0)
    # assert the user session is linked to the cookie
    cookie = test_get.headers.get('Set-Cookie')
    self.assertTrue(cookie and len(cookie) > 0)
    test_post = self.app.post(
      '/test', data='', headers={'X-XSRF-Token': token_string})
    self.assertEquals(test_post.status_code, 200)

  def test_app_request_w_bad_tokenstr_header_fails(self):
    test_post = self.app.post(
      '/test', data='', headers={'X-XSRF-Token': 'FAKE_STR'})
    self.assertEquals(test_post.status_code, 406)

  def test_app_request_w_bad_tokenstr_form_fails(self):
    """Assert invalid form token str fails properly."""
    test_get = self.app.get(
      '/test', data='', headers={})
    self.assertEquals(test_get.status_code, 200)
    test_post = self.app.post(
      '/test', data={'xsrf-token': 'FAKE_STR'}, headers={})
    self.assertEquals(test_post.status_code, 406)

  def test_app_request_w_valid_form_tokenstr_works(self):
    """Assert valid token string form works."""
    test_get = self.app.get(
      '/test', data='', headers={})
    self.assertEquals(test_get.status_code, 200)
    token_string = test_get.headers.get('X-XSRF-Token')
    test_post = self.app.post(
      '/test', data={'xsrf-token': token_string}, headers={})
    self.assertEquals(test_post.status_code, 200)

  def test_app_request_w_empty_header_and_form_tokenstr_works(self):
    """Assert empty header parses from form properly."""
    test_get = self.app.get(
      '/test', data='', headers={})
    self.assertEquals(test_get.status_code, 200)
    token_string = test_get.headers.get('X-XSRF-Token')
    test_post = self.app.post(
      '/test', data={'xsrf-token': token_string}, headers={
      'X-XSRF-Token': '' })
    self.assertEquals(test_post.status_code, 200)


if __name__ == '__main__':
  unittest.main()
