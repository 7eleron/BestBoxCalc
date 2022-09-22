import requests
from xml.dom import minidom


def currency_eur():
    try:
        data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
        return data['Valute']['EUR']['Value']
    except:
        return 0


def get_data(url):
    try:
        headers = {
            'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / avif, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3;q = 0.9',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
        }
        data = requests.get(url, headers=headers)
        return data.content
    except:
        return 0


def get_currency(Valute: str = 'EUR'):
    xml_contentent = get_data('http://www.cbr.ru/scripts/XML_daily.asp')
    dom = minidom.parseString(xml_contentent)
    dom.normalize()
    elements = dom.getElementsByTagName('Valute')
    currency_dict = {}
    for node in elements:
        for child in node.childNodes:
            if child.nodeType == 1:
                if child.tagName == 'Value' and child.firstChild.nodeType == 3:
                    value = float(child.firstChild.data.replace(',', '.'))
                if child.tagName == 'CharCode' and child.firstChild.nodeType == 3:
                    char_code = child.firstChild.data
        currency_dict[char_code] = value
    return currency_dict[Valute]


