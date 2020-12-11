import hhmain_parser as mp
import hhpage_parser as pp
from writers.hhabstract import *
import requests as rq
from bs4 import BeautifulSoup

class HHWebRequester():
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
        o_main_parser = mp.HHMainParser()
        o_page_parser = pp.HHPageParser()

        i_vacancy_number = 0
        # Устанавливаем связь с БД
        # Цикл по получению всех страниц с сайта
        while True:
            try:
                # Послать запрос на главный url
                o_response = rq.get(self._s_main_url, headers=self._d_headers)
                if o_response.status_code != 200 :
                    return o_response.status_code
            except Exception as ex:
                self._logger.error(f"Error during handling request for main page\n{ex}")
                raise ex

            # Пропускаем страницу поиска через парсер BeautifulSoup
            o_parsed = BeautifulSoup(o_response.text, "html.parser")
            l_urls = o_main_parser.parse(o_parsed)
            # При успешном ответе полученную страницу передаем в обработку парсеру страницы
            for url in l_urls:
                # Увеличиваем счетчик вакансий
                i_vacancy_number += 1
                try:
                    # Запрашиваем страницу вакансии
                    o_page_response = rq.get(url[1], headers=self._d_headers, verify=False)
                except Exception as ex:
                    self._logger.error(f"Error during handling request for vacancy page\n{ex}")
                    raise ex
                # Парсим страницу с помощью BeatifulSoup
                o_page_parsed = BeautifulSoup(o_page_response.text,"html.parser")

                # Парсим страницу с помощью HHPageParser
                d_result = o_page_parser.parse(o_page_parsed)

                # Если парсинг прошел удачно, то сохраняем результаты
                if d_result:
                    d_result["name"] = url[0]
                    # Записываем результаты парсинга
                    for writer in self._l_writer:
                        writer.write(d_result)

                    yield i_vacancy_number, d_result["vacancy_id"], 1
                else:
                    yield i_vacancy_number, url[1], 0

            # Находим кнопку "Дальше" и посылаем запрос, если кнопки нет, то завершаем цикл
            self._bs_page_next = o_parsed.find("a", attrs = {"data-qa":"pager-next"})
            if self._bs_page_next:
                self._s_main_url = self._d_headers['origin'] + self._bs_page_next["href"]
                continue
            else:
                break

    def close(self):
        """
            Метод очистки, должен запускаться перед удалением класса
        """
        for writer in self._l_writer:
            writer.close()
