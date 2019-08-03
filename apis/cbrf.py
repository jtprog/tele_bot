import datetime
from collections import namedtuple
from logging import getLogger

import xmltodict
import requests


logger = getLogger(__name__)


Rate = namedtuple('Rate', 'name,rate')


def str_to_float(item: str):
    item = item.replace(',', '.')
    return float(item)


def get_rate():
    # URL запроса
    get_curl = "http://www.cbr.ru/scripts/XML_daily.asp"
    # Формат даты: день/месяц/год
    date_format = "%d/%m/%Y"

    # Дата запроса
    today = datetime.datetime.today()
    params = {
        "date_req": today.strftime(date_format),
    }
    r = requests.get(get_curl, params=params)
    # TODO: обрабатывать ошибки от API

    resp = r.text

    # TODO: обрабатывать ошибки парсинга XML
    data = xmltodict.parse(resp)

    # Ищем по @ID
    section_id = 'R01235'

    # TODO: обрабатывать ошибки парсинга JSON
    for item in data['ValCurs']['Valute']:
        if item['@ID'] == section_id:
            r = Rate(
                name=item['CharCode'],
                rate=str_to_float(item['Value']),
            )
            return r
    return None
