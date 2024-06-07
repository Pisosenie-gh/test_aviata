from rocketry import Rocketry
from rocketry.conds import daily
import requests
import xmltodict
import json
from datetime import date

task_app = Rocketry(config={"task_execution": "async"})


@task_app.task(daily.after("12:00"))
def get_rates():
    today = date.today()
    url = f'https://www.nationalbank.kz/rss/get_rates.cfm?fdate={today.day}.{today.month}.{today.year}'
    response = requests.get(url)
    response_content = response.content
    rate_data = xmltodict.parse(response_content)
    json_data = json.dumps(rate_data, indent=4)

    with open("files/rate.json", "w") as json_file:
        json_file.write(json_data)
