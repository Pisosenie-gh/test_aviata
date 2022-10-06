
import json
import requests as r
import redis
from backend.views.services import get_rate
redis = redis.StrictRedis(host='redis', port=6379, db=0)

test_id = ""


def test_response_provider_a():
    response = r.post("http://localhost:8000/search")
    with open('files/response_a.json') as f:
        templates = json.load(f)
    assert response.status_code == 200
    assert response.json() == templates


def test_response_provider_b():
    response = r.post("http://localhost:8001/search")
    with open('files/response_b.json') as f:
        templates = json.load(f)
    assert response.status_code == 200
    assert response.json() == templates


def test_post_response_airflow():
    response = r.post("http://localhost:9000/search")
    assert response.status_code == 200
    assert response.json()["search_id"]
    global test_id
    test_id = response.json()["search_id"]

def test_redis():
    assert redis.set("test"," test_data")
    assert redis.get("test")
    assert redis.delete("test")


def test_get_response_airflow():
    response = r.get(f"http://localhost:9000/results/{test_id}/KZT")
    assert response.status_code == 200
    assert response.json()["status"] == "PENDING"



def test_get_response_airflow_bad_request():
    response = r.get(f"http://localhost:9000/results/ewqewqewqqfqdwq/KZT")
    assert response.status_code == 404

def test_rate():
    
    with open('files/rate.json') as f:
        templates = json.load(f)
    data = templates['rates']['item'][10]['description']
    assert get_rate("USD") == data


