import requests


def currency_eur():
    try:
        data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
        return data['Valute']['EUR']['Value']
    except:
        return 0

