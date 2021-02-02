import parsers.basic_parser as bp

"""
    Class VacancyURL parses html page to extract the data which 
    related to url of the open position
"""


class VacancyURLParser(bp.BaseParser):
    def parse(self, html_page, data_dict):
        for script in html_page.find_all("link",attrs={"rel": "canonical"}):
            data_dict["url"] = script.get("href")
            break
