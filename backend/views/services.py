import aiohttp
import json
import requests
import xmltodict
import redis
from datetime import date
redis = redis.StrictRedis(host='redis', port=6379, db=0)


# Получение курса валют к тенге.
def get_rate(currency):
    with open('files/rate.json') as f:
        templates = json.load(f)
    price = 0
    data = templates['rates']['item']
    for i in range(0, len(data)-1):
        if str(currency) in data[i]["title"]:
            price = data[i]['description']
            float(price)
        elif currency == "KZT":
            price = 1.0

    return price


# Отправка запросов в сервисы a и b.
async def get_response(search_id):
    a_url = 'http://provider_a:8000/search'
    b_url = 'http://provider_b:8001/search'
    async with aiohttp.ClientSession() as session:

        async with session.post(a_url) as resp:
            a_data = await resp.json()
            response_a = json.dumps(a_data)
            redis.set(str(search_id)+"_a", response_a)
        async with session.post(b_url) as resp:
            b_data = await resp.json()
            response_b = json.dumps(b_data)
            redis.set(str(search_id)+"_b", response_b)

# Cортировка ответов провайдеров и добавление поля Price.
async def sort_and_edit_json(search_id):
    response_a = json.loads(redis.get(str(search_id)+"_a"))
    response_b = json.loads(redis.get(str(search_id)+"_b"))
    print(len(response_a))
    for i in range(0, len(list(response_a))):
        price = response_a[i]["pricing"]["currency"]
        price = get_rate(price)
        total = response_a[i]["pricing"]["total"]
        total_price = float(total) * float(price)
        response_a[i]["price"] = {
            "amount": "%.2f" % total_price, "currency": "KZT"
            }

    for i in range(0, len(list(response_b))):
        price = response_b[i]["pricing"]["currency"]
        price = get_rate(price)
        total = response_b[i]["pricing"]["total"]
        total_price = float(total) * float(price)
        response_b[i]["price"] = {
            "amount": "%.2f" % total_price, "currency": "KZT"
            }
        response_a.append(response_b[i])

    response_a.sort(key=lambda x: float(x["price"]["amount"]))

    return response_a


def get_rates():
    d = date.today()
    url = f'https://www.nationalbank.kz/rss/get_rates.cfm?fdate={d.day}.{d.month}.{d.year}'
    r = requests.get(url)
    r = r.content
    dict_data = xmltodict.parse(r)
    json_object = json.dumps(dict_data, indent=4)
    with open("files/rate.json", "w") as outfile:
        outfile.write(json_object)