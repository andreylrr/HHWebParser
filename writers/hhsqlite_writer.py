import sqlite3 as sql
from writers.hhabstract import *


class HHSQLiteWriter(BaseWriter):
    def __init__(self, db_file, json_folder, logger):
        if not db_file:
            raise ValueError("Не указан путь к БД")
        self._s_db_file = db_file
        self._s_json_folder = json_folder
        self._logger = logger
        # Открываем БД
        try:
            self._db_connection = sql.connect(self._s_db_file)
            self._cursor = self._db_connection.cursor()
        except Exception as ex:
            logger.error(f"Error during establishing connection to DB\n {ex}")
            raise ex

    async def write(self, data):
        """
            Метод записи результатов парсинга в БД
        :param url: данные полученные после парсинга страницы поиска
        :param data: данные полиученные после парсинга страницы вакансии
        :param db_connection: объект БД
        """
        # Проверяем наличие вакансии с таки же номером в БД
        if self.check_vacancy_id(data):
            return

        # Получим номер региона
        try:
            i_region_id = self.get_region_id(data)
        except Exception as ex:
            self._logger.error(f"Error during getting region number\n{ex}")
            raise ex

        # Получим номера ключевых навыков
        try:
            l_skills_ids = self.get_skills_id(data)
        except Exception as ex:
            self._logger.error(f"Error during handling key skills\n{ex}")
            raise ex

        # Проверяем наличие имени файла в данных
        try:
            self.check_file_name(data)
        except Exception as ex:
            self._logger.error(f"Error during checking file name\n{ex}")
            raise ex

        # Заносим информацию о вакансии в БД
        try:
            sql = ''' INSERT INTO vacancies(id,name,url,file_name, min_salary, max_salary, region_id, experience, created)
                                      VALUES(?,?,?,?,?,?,?,?,datetime('now', 'localtime')) '''
            cur = self._cursor
            cur.execute(sql, (data["vacancy_id"], data.get("name"), data.get("url"), data.get("file_name"), data.get("min_salary"),
                              data.get("max_salary"), str(i_region_id), data.get("experience")))
            self._db_connection.commit()
        except Exception as ex:
            self._logger.error(f"Error during writing vacancy to DB\n{ex}")
            raise ex


        # Добавляем ключевые навыки
        try:
            self.add_skills(data["vacancy_id"], l_skills_ids)
        except Exception as ex:
            self._logger.error(f"Error during adding key skills to DB\n{ex}")
            raise ex


    def get_region_id(self, data):
        """
            Метод для получения региона
        :param data: даные полученные после парсинга
        :param db_connection: БД
        :return: номер региона
        """
        # Проверим регион на наличие в БД
        sql = '''SELECT id FROM regions WHERE city IS ? AND country IS ? AND region IS ?'''
        self._cursor.execute(sql, (data.get("city"), data.get("country"), data.get("region")))
        row = self._cursor.fetchone()

        # Если регион отсутствует в БД, то добавляем его в БД и читаем его номер из БД
        if not row:
            sql = '''INSERT INTO regions(city, country, region, created) VALUES(?,?,?,datetime('now','localtime'))'''
            self._cursor.execute(sql, (data.get("city"), data.get("country"), data.get("region")))
            self._db_connection.commit()

            sql = '''SELECT id FROM regions WHERE city IS ? AND country IS ? AND region IS ?'''
            self._cursor.execute(sql, (data.get("city"), data.get("country"), data.get("region")))
            row = self._cursor.fetchone()

        return row[0]

    def get_skills_id(self, data):
        """
            Метод получения номеров ключевых навыков
        :param data: данные полученные после парсинга
        :param db_connection: БД
        :return: списко ключевых навыков с их номерами
        """
        # Создаем курсор и лист с результатами
        l_skills_ids = []

        for skill in data["skills"]:
            # Осуществляем поиск ключевго навыка по его имени в БД
            sql = '''SELECT id FROM skills WHERE name = ?'''
            self._cursor.execute(sql, (skill,))
            row = self._cursor.fetchone()
            # Если ключевой навык не найден, то он заносится в БД
            if not row:
                sql = '''INSERT INTO skills(name, created) VALUES(?,datetime('now','localtime'))'''
                self._cursor.execute(sql, (skill,))
                self._db_connection.commit()

                sql = '''SELECT id FROM skills WHERE name = ?'''
                self._cursor.execute(sql, (skill,))
                row = self._cursor.fetchone()
            l_skills_ids.append(row[0])

        return l_skills_ids

    def add_skills(self, vacancy_id, skill_ids):
        """
            Добавляем к вакансии ключевые навыки
        :param vacancy_id: номер вакансии
        :param skill_ids: списко номеров ключевых навыков
        """
        for skill_id in skill_ids:
            sql = '''INSERT INTO skills_vacancies ( vacancy_id, skills_id) VALUES (?,?)'''
            self._cursor.execute(sql, (vacancy_id, skill_id))

        self._db_connection.commit()

    def check_file_name(self, data):
        """
            Метод проверяет наличие параметра с именем файла. Если он отсутсвует, то происходми его заполнение
        :param data: страница с вакансией в формате BeautifulSoup
        :return:
        """
        if not data.get("file_name"):
            data["file_name"] = self._s_json_folder + "/" + "vacancy_" + data["vacancy_id"]

    def check_vacancy_id(self, data):
        """
            Метод анализирует наличие вакансии с тем же номером в БД.
            Если вакансия уже присутствует, то ее обработка пропускается
        :param data: страница с вакансией в формате BeautifulSoup
        :return:
        """
        sql = '''SELECT id FROM vacancies WHERE id = ?'''
        self._cursor.execute(sql, (data.get("vacancy_id"),))
        row = self._cursor.fetchone()
        if row:
            return data["vacancy_id"]
        else:
            return None

    def close(self):
        """
            Метод закрывает связь с БД. Его нужно вызвать, перед уничтожением класса.
        :return:
        """
        self._cursor.close()
        self._db_connection.close()