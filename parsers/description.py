import parsers.basic_parser as bp

"""
    Class Description parses html page to extract the detailed description of the open position
"""


class DescriptionParser(bp.BaseParser):
    def parse(self, html_page, data_dict):
        for div in html_page.find_all("div"):
            if div.get("data-qa") == "vacancy-description":
                data_dict["description"] = div.text
                break
