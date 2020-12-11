import json
from writers.hhabstract import *
import io as io

"""
    Класс HHJsonWrite позволяет сохранять данные, которые были получены
    в результате парсинга в файл формата json
"""
class HHJsonWriter(BaseWriter):
    def __init__ (self, file_folder, logger):
        """
            Метод инициализации класса. Сохраняет входной параметр с каталогом,
            в который будут записаны файлы во внутренней переменной класса
        :param file_folder:
        """
        self._s_file_folder = file_folder
        self._logger = logger

    def write(self, data):
        """
             Метод записи результатов парсинга в файл json
        :param data: данные полученные из парсинга страницы вакансии
        :return: имя файла, если был задан путь, в противном случае None
        """
        # Если указано имя файла, то сохраняем результаты парсинга
        # в json файл
        if self._s_file_folder:
            try:
                # Формируем имя файла
                s_file_name = self._s_file_folder + "/" + "vacancy_" + data["vacancy_id"]
                # Записываем результаты парсинга в файл
                with io.open(s_file_name, 'w', encoding='utf-8') as json_file:
                    json.dump(data, json_file, ensure_ascii=False)
                return s_file_name
            except Exception as ex:
                self._logger.error(f"Error during writing vacancy to json file\n{ex}")
                raise ex
        return None

    def close(self):
        """
             Этот класс не требует дополнительных действий при уничтожении класса
        """
        return
