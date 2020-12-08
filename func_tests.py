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

class TestNumItems(TestCase):
    def test_get_num_items(self):
        with patch('requests.Response.json') as mock_request:
            url = 'http://facebook.com'
            mock_request.return_value = {'FHRSEstablishment': {'Header': {'ItemCount': '5'}}}
            expected_result = 5
            wrong_result = '5'
            response = f.get_num_items(url)
            self.assertEqual(response, expected_result)
            self.assertNotEqual(response, wrong_result)

class TestUrlCreator(TestCase):
    def test_url_creator(self):
        test_code = 43
        expected_url = 'http://ratings.food.gov.uk/enhanced-search/en-GB/^/^/ALPHA/0/43/1/30/json'
        self.assertEqual(f.url_creator(test_code), expected_url)
        self.assertEqual(type(f.url_creator(test_code)), str)







if __name__ == '__main__':
    unittest.main()