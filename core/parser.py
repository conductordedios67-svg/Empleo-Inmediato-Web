from bs4 import BeautifulSoup


def obtener_titulo(html):

    soup = BeautifulSoup(html, "lxml")

    return soup.title.text
