import parsers.basic_parser as bp

"""
    Class VacancyIdParser parses html page to extract the data which 
    related to ID of the open position
"""


class VacancyIDParser(bp.BaseParser):
    def parse(self, html_page, data_dict):
        for script in html_page.find_all("link",attrs={"rel": "canonical"}):
            l_ids = script.get("href").split("/")
            data_dict["vacancy_id"] = l_ids[-1]
            break
