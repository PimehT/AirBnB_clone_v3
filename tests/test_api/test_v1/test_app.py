#!/usr/bin/python3
"""
Contains tests for api/v1/app.py.
"""
import os
import unittest
import pycodestyle
from tests.test_api.test_v1.base_test import BaseTestCase
from api.v1 import app as app_py


class TestAppDocs(unittest.TestCase):
    """Tests to check the documentation and style app.py."""

    def test_pep8_conformance_app(self):
        """Test that api/v1/app.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/app.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_app_module_docstring(self):
        """Test for the api/v1/app.py module docstring"""
        self.assertIsNot(app_py.__doc__, None,
                         "api/v1/app.py needs a docstring")
        self.assertTrue(len(app_py.__doc__) >= 1,
                        "api/v1/app.py needs a docstring")


class TestApp(BaseTestCase):
    """Test the App module."""

    def test_response_code_success(self):
        """Test that upon success, 200 is returned."""
        resp = self.client.get('/api/v1/status')
        msg = "Response code of 'GET HTTP 1.0 /api/v1/status' should be 200 OK"
        self.assertEqual(200, resp.status_code, msg=msg)

    def test_response_return_type(self):
        """Test that response is json."""
        resp = self.client.get('/api/v1/status')
        self.assertTrue(resp.is_json)
        self.assertEqual(resp.headers.get('Content-Type'), "application/json")

    def test_error_handler_404_response(self):
        """Test 404 error."""
        resp = self.client.get('/not_found')
        self.assertEqual({'error': 'Not found'}, resp.json)

    def test_error_404_status_code(self):
        """Test that upon 404 status code is 404."""
        resp = self.client.get('/not_found')
        self.assertEqual(404, resp.status_code)

    def test_cors(self):
        """Test CORS."""
        resp = self.client.get('/api/v1/status')
        header = 'Access-Control-Allow-Origin'
        resp_header = resp.headers.get('Access-Control-Allow-Origin')
        self.assertIsNotNone(resp_header)
        self.assertEqual(resp.headers.get(header), "0.0.0.0",
                         msg="Response header {header} not '0.0.0.0'")
