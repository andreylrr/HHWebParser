from bs4 import BeautifulSoup

class HHPageParser():
    def __init__(self):
        self._bs_page = None
        self._d_result = None

    def parse(self, bs_page):

        self._d_result = dict()
        self._bs_page = bs_page
        if self._bs_page == None:
            raise ValueError("Нет страницы для парсинга.")

        self.get_vacancy_id()

        self.get_publication_date()
        if not self._d_result.get("datePosted"):
           return None

        self.get_vacancy_url()
        self.get_region()
        self.get_experience()
        self.get_salary()
        self.get_keyskills()
        self.get_description()

        return self._d_result

    def get_region(self):
        """
             Метод извлекает из страницы регион, где находится вакансия
             и записывает его в словарь результатов
        """
        for meta in self._bs_page.find_all("meta"):
            if meta.get("itemprop") == "addressLocality":
                self._d_result["city"] = meta["content"]
            if meta.get("itemprop") == "addressRegion":
                self._d_result["region"] = meta["content"]
            if meta.get("itemprop") == "addressCountry":
                self._d_result["country"] = meta["content"]

    def get_experience(self):
        s_experience = None
        for span in self._bs_page.find_all("span"):
            if span.get("data-qa") == "vacancy-experience":
                s_experience = span.text
                break
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

    def get_publication_date(self):
        for meta in self._bs_page("meta"):
            if meta.get("itemprop") == "datePosted":
                self._d_result["datePosted"] = meta["content"]
                break

    def get_salary(self):
        bs_found = self._bs_page.find("meta",attrs={"itemprop": "currency"})
        if bs_found:
            self._d_result["salary_currency"] = bs_found.get("content")
        bs_found = self._bs_page.find("meta",attrs={"itemprop": "minValue"})
        if bs_found:
            self._d_result["min_salary"] = bs_found.get("content")
        bs_found = self._bs_page.find("meta", attrs={"itemprop": "maxValue"})
        if bs_found:
            self._d_result["max_salary"] = bs_found.get("content")

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

if __name__ == "__main__":
    # This code was used only for testing purposes
    hhpage = HHPageParser()
    f = open("Test/page.html",mode="r", encoding="utf-8")
    bs_html = BeautifulSoup(f,"html.parser")
    print(hhpage.parse(bs_html))


