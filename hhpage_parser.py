from bs4 import BeautifulSoup
import json

class HHPageParser():
    def __init__(self):
        self._bs_page = None
        self._d_result = None

    def parse(self, bs_page):

        self._d_result = dict()
        self._bs_page = bs_page
        if not self._bs_page:
            raise ValueError("Нет страницы для парсинга.")

        if self.is_valid():
            self.get_title()
            self.get_vacancy_id()
            self.get_vacancy_url()
            self.get_region()
            self.get_experience()
            self.get_salary()
            self.get_keyskills()
            self.get_description()
            self.get_prof_specs()

        return self._d_result

    def get_region(self):
        """
             Метод извлекает из страницы регион, где находится вакансия
             и записывает его в словарь результатов
        """
        src = self._bs_page.find("script", attrs={"data-name":"HH/GoogleDfpService"})
        vac_city = ""
        if src:
            dtext = src.get("data-params")
            if dtext:
                src: json = json.loads(dtext)
                vac_city = src["vac_city"]
        self._d_result["vac_city"] = vac_city

        for meta in self._bs_page.find_all("meta"):
                if meta.get("itemprop") == "addressLocality":
                    self._d_result["city"] = meta["content"]
                if meta.get("itemprop") == "addressRegion":
                    self._d_result["region"] = meta["content"]
                if meta.get("itemprop") == "addressCountry":
                    self._d_result["country"] = meta["content"]

    def is_valid(self):
        for h2 in self._bs_page.find_all("h2"):
            if h2.get("data-qa") == "bloko-header-2":
                if h2.text == "Вакансия в архиве":
                    return False

        if not self._bs_page.find("script", attrs={"data-name":"HH/GoogleDfpService"}):
            return False
        return True

    def get_prof_specs(self):
        """
             Метод извлекает из страницы специальность и проф обл.
             и записывает их в словарь результатов
        """
        src = self._bs_page.find("script", attrs={"data-name":"HH/GoogleDfpService"})
        if src:
            dtext = src.get("data-params")
            if dtext:
                src = json.loads(dtext)
                self._d_result["specs"] = src["vac_specs"]
                self._d_result["prof"] = src["vac_profarea"]


    def get_experience(self):
        s_experience = None
        for span in self._bs_page.find_all("span"):
            if span.get("data-qa") == "vacancy-experience":
                s_experience = span.text
                break
        if s_experience :
            if s_experience == "не требуется":
                self._d_result["experience"] = "0"
            elif s_experience.startswith("более"):
                self._d_result["experience"] = s_experience.split(" ")[1]
            elif s_experience.startswith("от"):
                self._d_result["experience"] = s_experience.split(" ")[1]
            else:
                l_exp_split = s_experience.split(" ")
                l_exp_split = l_exp_split[0].split("–")

                for s_exp in l_exp_split:
                    if s_exp.isdigit():
                        self._d_result["experience"] = s_exp
                        break

    def get_keyskills(self):
        l_skills = []
        for span in self._bs_page.find_all("span"):
            if span.get("data-qa") == "skills-element":
                l_skills.append(span.get("data-tag-id"))
        self._d_result["skills"] = l_skills

    def get_salary(self):
        src = self._bs_page.find("script", attrs={"data-name":"HH/GoogleDfpService"})
        if src:
            dtext = src.get("data-params")
            if dtext:
                src = json.loads(dtext)
                self._d_result["min_salary"] = src["vac_salary_from"]
                self._d_result["max_salary"] = src["vac_salary_to"]
                self._d_result["salary_currency"] = src["vac_salary_cur"]

    def get_description(self):
        for div in self._bs_page.find_all("div"):
            if div.get("data-qa") == "vacancy-description":
                self._d_result["description"] = div.text
                break

    def get_vacancy_id(self):
        for script in self._bs_page.find_all("link",attrs={"rel": "canonical"}):
            l_ids = script.get("href").split("/")
            self._d_result["vacancy_id"] = l_ids[-1]
            break

    def get_vacancy_url(self):
        for script in self._bs_page.find_all("link",attrs={"rel": "canonical"}):
            self._d_result["url"] = script.get("href")
            break


    def get_title(self):
        for h1 in self._bs_page.find_all("h1"):
            if h1.get("data-qa") == "vacancy-title":
                self._d_result["name"] = h1.text
