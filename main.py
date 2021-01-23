import urllib3
from hhweb_requester_full import HHWebRequesterFull
from writers.hhpostgres_writer import HHPostgresWriter
from writers.hhjson_writer import HHJsonWriter
import configparser as cfg
import json
import logging
import logging.config
from requests import get
import asyncio


async def main():
    # Блокируем вывод сообщений с уровнем Warning
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Инициализируем парсер для конфигурационного файла
    config = cfg.ConfigParser()
    config.read("hh_config.ini")

    logging.config.fileConfig('hh_config.ini')
    logging.FileHandler.encoding = "UTF-8"
    logger = logging.getLogger("HHAnalytics")
    logger.info("HHAnalytics started")

    # Читаем начальные параметры из конфигурационного файла
    url_with_request = config["Request"]["url"]
    db_string = config["PostgreSQL"]["db_string"]
    file_folder = config["Json"]["path"]
    with open(config["Request"]["header"], "r") as f:
        headers = json.load(f)
    logger.info("Configuration file has been read")

    # Создаем класс обработки запросов
    web_requester = HHWebRequesterFull(logger)
    web_requester.set_main_url(url_with_request)
    web_requester.set_headers(headers)
    logger.info("HHWebRequest class has been constructed")

    # Получаем справочник регионов
    json_ref_reg = get("https://api.hh.ru/areas", headers=headers, verify=False)
    json_ref_reg = json.loads(json_ref_reg.content)

    # Создаем классы обработки записи результатов парсинга
    sql_writer = HHPostgresWriter(db_string, file_folder, logger, json_ref_reg)
    json_writer = HHJsonWriter(file_folder, logger)
    web_requester.add_writer(sql_writer)
    web_requester.add_writer(json_writer)
    logger.info("Classes that support writing vacancies to different outputs have been created.")

    # Запускаем обработку запроса
    logger.info("Request handling started")
    await asyncio.gather(web_requester.process(logger))

    # Очищаем все ресуры
    web_requester.close()
    logger.info("All resources have been released")


if __name__ == "__main__":
    asyncio.run(main())
