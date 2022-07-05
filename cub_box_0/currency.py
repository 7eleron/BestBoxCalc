import requests


def currency_eur():
    data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    return data['Valute']['EUR']['Value']
