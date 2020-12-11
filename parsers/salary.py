import parsers.basic_parser as bp
import json

"""
    Class Salary parses html page to extract the data which 
    related to the proposed salary for the open position
"""


class Experience(bp.BaseParser):
    def parse(self, html_page, data_dict):
        src = html_page.find("script", attrs={"data-name":"HH/GoogleDfpService"})
        if src:
            d_text = src.get("data-params")
            if d_text:
                src = json.loads(d_text)
                data_dict["min_salary"] = src["vac_salary_from"]
                data_dict["max_salary"] = src["vac_salary_to"]
                data_dict["salary_currency"] = src["vac_salary_cur"]

