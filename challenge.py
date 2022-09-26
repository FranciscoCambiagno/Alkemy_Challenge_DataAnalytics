from bs4 import BeautifulSoup
import csv
import requests
import ast

def ObtenerCSV():
    url = PrepararURL('https://docs.google.com/spreadsheets/d/1o8QeMOKWm4VeZ9VecgnL8BWaOlX5kdCDkXoAph37sQM/edit#gid=1691373423')

    html = requests.get(url).text
    soup = BeautifulSoup(html, "lxml")
    tables = soup.find_all("table")
    index = 0
    for table in tables:
        with open(str(index) + ".csv", "w", encoding='utf8') as f:
            wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
            wr.writerows([[td.text for td in row.find_all("td")] for row in table.find_all("tr")])
        index = index + 1

def PrepararURL(url):
    """
    Prepara el url para poder hacer web scraping sin la limitacion de 100 filas de google sheets
    """

    ultimo_slash = url.rfind("/")
    anteultimo_slash = url.rfind("/", 0, ultimo_slash)

    recorte_url = url[anteultimo_slash +1: ultimo_slash]

    return "https://spreadsheets.google.com/tq?tqx=out:html&tq=&key=" + recorte_url

def run():
    """
    Es el cuerpo del programa
    """
    ObtenerCSV()


if __name__ == "__main__":
    run()