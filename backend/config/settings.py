import redis

redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

PROVIDER_A_URL = "http://provider_a:8000/search"
PROVIDER_B_URL = "http://provider_b:8001/search"
data = []