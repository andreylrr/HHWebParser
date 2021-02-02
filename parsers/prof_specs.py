import parsers.basic_parser as bp
import json

"""
    Class ProfSpecs parses html page to extract the data which 
    related to professional specifications of the open position
"""


class ProfSpecParser(bp.BaseParser):
    def parse(self, html_page, data_dict):
        src = html_page.find("script", attrs={"data-name":"HH/GoogleDfpService"})
        if src:
            d_text = src.get("data-params")
            if d_text:
                src = json.loads(d_text)
                data_dict["specs"] = src["vac_specs"]
                data_dict["prof"] = src["vac_profarea"]
