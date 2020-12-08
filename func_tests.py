from unittest import TestCase
import unittest
import requests
from unittest.mock import patch
from main import FoodRater
import json
f = FoodRater()
class TestResponse(TestCase):
    def test_response(self):
        with patch('requests.Response.json') as mock_request:
            url = 'http://facebook.com'
            mock_request.return_value.json = {"Fake: content"}
            mock_request.return_value.status_code = 200
            response = f.get_response(url)
            self.assertEqual(response, mock_request.return_value)
            self.assertEqual(response.status_code, mock_request.return_value.status_code)

class TestPageCount(TestCase):
    def test_page_count(self):
        dummy_number = 6790
        expected_result = 2
        self.assertEqual(f.get_page_count(dummy_number), expected_result)




if __name__ == '__main__':
    unittest.main()