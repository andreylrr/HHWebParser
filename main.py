import urllib3
from hhweb_requester_full import HHWebRequesterFull
from hhpostgres_writer import HHPostgresWriter
from hhjson_writer import HHJsonWriter
import sys
import configparser as cfg
import json
import logging
import logging.config
from requests import get


def main():
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
    s_url_with_request = config["Request"]["url"]
    s_db_string = config["PostgreSQL"]["db_string"]
    s_file_folder = config["Json"]["path"]
    f = open(config["Request"]["header"], "r")
    d_headers = json.load(f)
    f.close()
    logger.info("Configuration file has been read")

    # Создаем класс обработки запросов
    o_web_requester = HHWebRequesterFull(logger)
    o_web_requester.set_main_url(s_url_with_request)
    o_web_requester.set_headers(d_headers)
    logger.info("HHWebRequest class has been constructed")

    # Получаем справочник регионов
    o_json_ref_reg = get("https://api.hh.ru/areas", headers=d_headers, verify=False)
    o_json_ref_reg = json.loads(o_json_ref_reg.content)

    # Создаем классы обработки записи результатов парсинга
    o_sql = HHPostgresWriter(s_db_string, s_file_folder, logger, o_json_ref_reg)
    o_json = HHJsonWriter(s_file_folder, logger)
    o_web_requester.add_writer(o_sql)
    o_web_requester.add_writer(o_json)
    logger.info("Classes that supports writing vacancy to different sources have been created.")

    # Запускаем обработку запроса
    logger.info("Request handling started")
    it_parser = o_web_requester.process()
    for number, vac_id, code in it_parser:
        sys.stdout.write("\r")
        if code == 1:
            sys.stdout.write(f"Обработана вакансия {number} с номером {vac_id}")
            logger.info(f"Vacancy {number} with number {vac_id} was handled.")
        else:
            sys.stdout.write(f"Вакансия {number} с номером {vac_id} имеет не стандартный формат и была пропущена")
            logger.info(f"Vacancy {number} with number {vac_id} didn't have the right format and has been skipped")

    # Очищаем все ресуры
    o_web_requester.close()
    logger.info("All resources have been released")


if __name__ == "__main__":
    main()
