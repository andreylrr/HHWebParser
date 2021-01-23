import hhpage_parser as pp
from writers.hhabstract import BaseWriter
import requests as rq
from bs4 import BeautifulSoup
import aiohttp
import sys
import asyncio
from fake_headers import Headers

class HHWebRequesterFull():
    def __init__(self, logger):
        self._main_url = None
        self._headers = None
        self._writers = []
        self._logger = logger

    def set_main_url(self, url):
        self._main_url = url

    def set_headers(self, headers):
        self._headers = headers

    def add_writer(self, writer: BaseWriter):
        self._writers.append(writer)

    async def process(self, logger):
        """
             Метод обработки парсинга основной страницы поиска и
             страницы вакансии
        :return:
        """
        # Проверяем наличие всех входных параметров, необходимых для парсинга
        if not self._main_url:
            self._logger.error(f"Url to the main page needs to be specified")
            raise ValueError("Необходимо установить url основного запроса")

        # Создаем парсеры для парсинга страницы поиска и страницы вакансии
        self._page_parser = pp.HHPageParser()

        l_urls = str.split(self._main_url, "/")
        self._main_url = "/".join(l_urls[:-1])

        vacancy_number = 37103645 #36950000
        # Устанавливаем связь с БД
        # Цикл по получению всех страниц с сайта

        self._headers = Headers(headers=True)

        while True:

            tasks = list()
            for i in range(vacancy_number, 6):
                vacancy_url = self._main_url + "/" + str(i)
                tasks.append(asyncio.create_task(self.process_vacancy(vacancy_url, i, logger)))
            await asyncio.gather(tasks)

            vacancy_number += 5

    async def process_vacancy(self, url, vacancy_number, logger):

        try:

            # Запрашиваем страницу вакансии
            page_response = rq.get(url, headers=self._headers.generate(), verify=False)
        except Exception as ex:
            self._logger.error(f"Error during handling request for vacancy page\n{ex}")
            raise ex

        sys.stdout.write("\r")

        if page_response.status_code == 200:

            # Парсим страницу с помощью BeatifulSoup
            page_parsed = BeautifulSoup(page_response.text, "html.parser")

            # Парсим страницу с помощью HHPageParser
            data_from_parsing = self._page_parser.parse(page_parsed)

            # Если парсинг прошел удачно, то сохраняем результаты
            if data_from_parsing:

                tasks = list()
                # Записываем результаты парсинга
                for writer in self._writers:
                    tasks.append(asyncio.create_task(writer.write(data_from_parsing)))
                await asyncio.gather(tasks)

                sys.stdout.write(f"Обработана вакансия {self._vacancy_url} с номером {vacancy_number}")
                logger.info(f"Vacancy {self._vacancy_url} with number {vacancy_number} was handled.")
            else:
                sys.stdout.write(f"Вакансия {self._vacancy_url} с номером {vacancy_number} имеет не стандартный формат и была пропущена")
                logger.info(f"Vacancy {self._vacancy_url} with number {vacancy_number} didn't have the right format and has been skipped")
        else:
            sys.stdout.write(f"При получкнии вакансии {self._vacancy_url} с номером {vacancy_number} произошла ошибка. Код ошибки({page_response.status_code}")
            logger.info(f"During reading vacancy {self._vacancy_url} with number {vacancy_number} an error occurred. Error Code({page_response.status_code}")

    def close(self):
        """
            Метод очистки, должен запускаться перед удалением класса
        """
        for writer in self._writers:
            writer.close()
