import parsers.basic_parser as bp

"""
    Class TitleParser parses html page to extract the data which 
    related to the title of the open position
"""


class TitleParser(bp.BaseParser):
    def parse(self, html_page, data_dict):
        for h1 in html_page.find_all("h1"):
            if h1.get("data-qa") == "vacancy-title":
                data_dict["name"] = h1.text
