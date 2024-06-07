import json
import requests as r
from config.settings import redis_client
import unittest
from utils.rate import get_rate


class TestServiceResponses(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_id = ""

    def test_response_provider_a(self):
        response = r.post("http://localhost:8000/search")
        with open('files/response_a.json') as f:
            templates = json.load(f)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), templates)

    def test_response_provider_b(self):
        response = r.post("http://localhost:8001/search")
        with open('files/response_b.json') as f:
            templates = json.load(f)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), templates)

    def test_post_response_airflow(self):
        response = r.post("http://localhost:9000/search")
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_id", response.json())
        self.__class__.test_id = response.json()["search_id"]

    def test_redis(self):
        self.assertTrue(redis_client.set("test", "test_data"))
        self.assertEqual(redis_client.get("test"), b"test_data")
        self.assertTrue(redis_client.delete("test"))

    def test_get_response_airflow(self):
        response = r.get(f"http://localhost:9000/results/{self.__class__.test_id}/KZT")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "PENDING")

    def test_get_response_airflow_bad_request(self):
        response = r.get("http://localhost:9000/results/ewqewqewqqfqdwq/KZT")
        self.assertEqual(response.status_code, 404)

    def test_rate(self):
        with open('files/rate.json') as f:
            templates = json.load(f)
        expected_rate = float(templates['rates']['item'][10]['description'])
        self.assertEqual(get_rate("USD"), expected_rate)

if __name__ == '__main__':
    unittest.main()