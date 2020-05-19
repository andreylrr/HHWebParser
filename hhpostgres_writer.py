# coding=utf-8
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from hhabstract import BaseWriter
import sqlalchemy as db
from postgres_model import Regions, Vacancies, Skills, ProfArea, ProfSpecs
import datetime
from sqlalchemy.orm.attributes import flag_modified


class HHPostgresWriter(BaseWriter):

    def __init__(self, db_string, json_folder, logger, ref_regions):
        if not db_string:
            raise ValueError("Не указан путь к БД")
        self._db_engine = db.create_engine(db_string)
        self._s_json_folder = json_folder
        self._logger = logger
        self._ref_regions = ref_regions
        self._vac_found = []
        # Открываем БД
        try:
            self._db_connection = self._db_engine.connect()
        except Exception as ex:
            logger.error(f"Error during establishing connection to PostgreSQL database\n {ex}")
            raise ex

        Session = sessionmaker()
        Session.configure(bind=self._db_engine)
        self._session = Session()

    def write(self, data):
        """
            Метод записи результатов парсинга в БД
        :param url: данные полученные после парсинга страницы поиска
        :param data: данные полиученные после парсинга страницы вакансии
        :param db_connection: объект БД
        """
        # Проверяем наличие вакансии с таки же номером в БД
        if self.check_vacancy_id(data):
            return

        # Получим регион
        try:
            region = self.get_region(data)
        except Exception as ex:
            self._logger.error(f"Error during getting region number\n{ex}")
            raise ex

        # Добавим ключевые навыки к вакансии
        try:
            l_skills = self.get_skills_id(data)
        except Exception as ex:
            self._logger.error(f"Error during handling key skills\n{ex}")
            raise ex

        mi_sal = data.get("min_salary").strip()
        mx_sal = data.get("max_salary").strip()

        # Создадим вакансию
        self._vac_new = Vacancies(data.get("vacancy_id"), data.get("name"), data.get("url"), data.get("file_name"),
                                  int(mi_sal) if mi_sal else 0,
                                  int(mx_sal) if mx_sal else 0,
                                  data.get("salary_currency"),
                                  data.get("experience"),)

        self._vac_new.region = region
        self._vac_new.prof_areas = self.add_prof_area(data.get("prof"))
        self._vac_new.prof_specs = self.add_prof_spec(data.get("specs"))
        self._vac_new.skills = l_skills

        # Проверяем наличие имени файла в данных
        try:
            self.check_file_name(data)
        except Exception as ex:
            self._logger.error(f"Error during checking file name\n{ex}")
            raise ex

        self._session.add(self._vac_new)
        self._session.commit()

    def add_prof_area(self, ids):
        list_area = []
        for id in ids:
            prof_area_found = self._session.query(ProfArea).filter(ProfArea.id == id).first()
            if prof_area_found:
                list_area.append(prof_area_found)
        return list_area

    def add_prof_spec(self, ids):
        list_spec = []
        for id in ids:
            prof_specs_found = self._session.query(ProfSpecs).filter(ProfSpecs.id == id).first()
            if prof_specs_found:
                list_spec.append(prof_specs_found)
        return list_spec

    def get_region(self, data):
        """
            Метод для получения региона
        :param data: даные полученные после парсинга
        :return: номер региона
        """
        reg_found = self._session.query(Regions).filter(Regions.vac_city == data.get("vac_city")).first()
        if not reg_found:
            vacs = data.get("vac_city").split(".")
            regions = []
            for vac in vacs:
                if not vac: continue
                self.vac_search(vac, self._ref_regions, regions)

            if len(regions) > 2:
                reg_record = Regions(regions[-1][0], regions[0][0], regions[1][0],
                                     data.get("vac_city"), datetime.datetime.now())
            else:
                reg_record = Regions(regions[-1][0], regions[0][0], regions[-1][0],
                                     data.get("vac_city"), datetime.datetime.now())

            self._session.add(reg_record)
            self._session.commit()
            reg = reg_record
        else:
            reg = reg_found

        return reg

    def vac_search(self, vac_code, areas, regions):
        """
            Поиск региона по vac коду
        :param vac_code: часть vac кода найденная во время парсинга страницы
        :param areas: часть справочника, где происходит поиск vac кода
        :param regions: список всех расшифрованных регионов
        :return: название региона и его отцовский id
        """
        for area in areas:
            if not area: return None
            if area["id"] == vac_code:
               return regions.append([area["name"], area["parent_id"]])
            self.vac_search(vac_code, area["areas"], regions)

    def get_skills_id(self, data):
        """
            Метод получения номеров ключевых навыков
        :param data: данные полученные после парсинга
        :param db_connection: БД
        :return: списко ключевых навыков с их номерами
        """
        # Создаем лист с результатами
        l_skills = []

        for skill in data["skills"]:
            skill_found = self._session.query(Skills).filter(Skills.name == skill).first()
            if not skill_found:
                self._session.add(Skills(skill, datetime.datetime.now()))
                self._session.commit()
                skill_found = self._session.query(Skills).filter(Skills.name == skill).first()
            l_skills.append(skill_found)

        return l_skills

    def check_file_name(self, data):
        """
            Метод проверяет наличие параметра с именем файла. Если он отсутсвует, то происходми его заполнение
        :param data: страница с вакансией в формате BeautifulSoup
        :return:
        """
        if not data.get("file_name"):
            data["file_name"] = self._s_json_folder + "/" + "vacancy_" + data["vacancy_id"]
        self._vac_new.file_name = data["file_name"]

    def check_vacancy_id(self, data):
        """
            Метод анализирует наличие вакансии с тем же номером в БД.
            Если вакансия уже присутствует, то ее обработка пропускается
        :param data: страница с вакансией в формате BeautifulSoup
        :return:
        """
        vac_found = self._session.query(Vacancies).filter(Vacancies.id == data.get("vacancy_id")).first()

        if vac_found:
            return data["vacancy_id"]
        else:
            return None

    def close(self):
        """
            Метод закрывает связь с БД. Его нужно вызвать, перед уничтожением класса.
        :return:
        """
        # self._cursor.close()
        self._db_connection.close()
