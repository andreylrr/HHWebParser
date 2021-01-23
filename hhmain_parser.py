import sqlite3 as sql
from bs4 import BeautifulSoup

"""
    Этот класс используется для извлечения всех ссылок на вакансий на
    html странице с сайта Head Hunter.

"""
class HHMainParser():
    def __init__(self):
        self._bs_page = None

    def parse(self, bs_page):
        """
             Метод, в котором происходит парсинг поисковой страницы
        :param bs_page: поисковая страница в формате BeautifulSoup
        :return:
        """
        self._bs_page = bs_page
        l_data = []

        if self._bs_page == None:
            raise ValueError("Страница для парсинга не определена")

        # Найти все urls и номера вакансий
        for link in bs_page.find_all("a"):
            if link.get("data-qa") == "vacancy-serp__vacancy-title":
                # Найти url ссылку на вакансию
                self._url = link.attrs["href"]
                # Найти название вакансии
                self._name = link.text
                # Сохранить данные для возврата
                l_data.append((self._name, self._url))

        return l_data

if __name__ == "__main__":
    # This code was used only for testing purposes
    hhmain = HHMainParser()
    connection = sql.connect("Database/hh_database.db")
    f = open("Test/main.html",mode="r", encoding="utf-8")
    bs_html = BeautifulSoup(f,"html.parser")
    print(hhmain.parse(bs_html))
