import requests
import pandas as pd
import tabula

"""
def pdf_list(url):
    response = requests.get(url)
    with open('metadata.pdf', 'wb') as f:
        f.write(response.content)
pdf_list("https://www.doublev.ru/upload/prices/price_%D0%B4%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD%D0%B5%D1%80%D1%81%D0%BA%D0%B8%D0%B5%20%D0%B1%D1%83%D0%BC%D0%B0%D0%B3%D0%B8%20%D0%B8%20%D0%BA%D0%BE%D0%BD%D0%B2%D0%B5%D1%80%D1%82%D1%8B.pdf")
"""


def pdf_text(url):
    pdf_in = url
    PDF = tabula.read_pdf(pdf_in, pages=19, multiple_tables=True)
    print(PDF)
    with open('data.csv', 'wb') as f:
        PDF = pd.DataFrame(PDF)
        PDF.to_csv(f)
    print("Done")


pdf_text('metadata.pdf')
