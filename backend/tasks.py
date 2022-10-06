from rocketry import Rocketry
from rocketry.conds import daily
import requests
import xmltodict
import json
from datetime import date
from views.services import get_rates as get_r

task_app = Rocketry(config={"task_execution": "async"})

# Загрузка курса при запуске, каждый день в 12:00.
@task_app.task(daily.after("12:00"))
def get_rates():
    d = date.today()
    url = f'https://www.nationalbank.kz/rss/get_rates.cfm?fdate={d.day}.{d.month}.{d.year}'
    r = requests.get(url)
    r = r.content
    dict_data = xmltodict.parse(r)
    json_object = json.dumps(dict_data, indent=4)
    with open("files/rate.json", "w") as outfile:
        outfile.write(json_object)
  
def start():
    task_app.run()
