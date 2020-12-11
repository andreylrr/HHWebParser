import hhpage_parser as pp
from writers.hhabstract import BaseWriter
import requests as rq
from bs4 import BeautifulSoup

class HHWebRequesterFull():
    def __init__(self, logger):
        self._s_main_url = None
        self._d_headers = None
        self._l_writer = []
        self._logger = logger

    def set_main_url(self, url):
        self._s_main_url = url

    def set_headers(self, headers):
        self._d_headers = headers

    def add_writer(self, writer: BaseWriter):
        self._l_writer.append(writer)

    def process(self):
        """
             Метод обработки парсинга основной страницы поиска и
             страницы вакансии
        :return:
        """
        # Проверяем наличие всех входных параметров, необходимых для парсинга
        if self._s_main_url == None:
            self._logger.error(f"Url to the main page needs to be specified")
            raise ValueError("Необходимо установить url основного запроса")

        # Создаем парсеры для парсинга страницы поиска и страницы вакансии
        o_page_parser = pp.HHPageParser()

        l_urls = str.split(self._s_main_url,"/")
        self._s_main_url = "/".join(l_urls[:-1])

        i_vacancy_number = 37103645 #36950000
        # Устанавливаем связь с БД
        # Цикл по получению всех страниц с сайта
        while True:

            self._s_vacancy_url = self._s_main_url + "/" + str(i_vacancy_number)

            try:
                # Запрашиваем страницу вакансии
                o_page_response = rq.get(self._s_vacancy_url, headers=self._d_headers, verify=False)
            except Exception as ex:
                self._logger.error(f"Error during handling request for vacancy page\n{ex}")
                raise ex

            if o_page_response.status_code == 200:

                # Парсим страницу с помощью BeatifulSoup
                o_page_parsed = BeautifulSoup(o_page_response.text,"html.parser")

                # Парсим страницу с помощью HHPageParser
                d_result = o_page_parser.parse(o_page_parsed)

                # Если парсинг прошел удачно, то сохраняем результаты
                if d_result:
                    # Записываем результаты парсинга
                    for writer in self._l_writer:
                        writer.write(d_result)

                    yield i_vacancy_number, self._s_vacancy_url, 1
                else:
                    yield i_vacancy_number, self._s_vacancy_url, 2
            else:
                yield i_vacancy_number, self._s_vacancy_url, o_page_response.status_code

            i_vacancy_number += 1

    def close(self):
        """
            Метод очистки, должен запускаться перед удалением класса
        """
        for writer in self._l_writer:
            writer.close()
