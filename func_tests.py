from unittest import TestCase
import unittest
import requests
from unittest.mock import patch
from main import FoodRater
import json
f = FoodRater()
class TestResponse(TestCase):
    def test_response(self):
        with patch('requests.get') as mock_request:
            url = 'http://facebook.com'

           
            mock_request.return_value.response = "Fake content"
            mock_request.return_value.json = "Fake content"
            mock_request.return_value.status_code = 200
            response = f.return_response(url)
            print(type(response))
            self.assertEqual(response.response, mock_request.return_value.response)

if __name__ == '__main__':
    unittest.main()