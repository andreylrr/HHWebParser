import parsers.basic_parser as bp
import json

"""
    Class Region parses html page to extract the data which 
    related to url of the open position
"""


class RegionParser(bp.BaseParser):
    def parse(self, html_page, data_dict):
        src = html_page.find("script", attrs={"data-name": "HH/GoogleDfpService"})
        vac_city = ""
        if src:
            d_text = src.get("data-params")
            if d_text:
                src: json = json.loads(d_text)
                vac_city = src["vac_city"]
        data_dict["vac_city"] = vac_city

        for meta in html_page.find_all("meta"):
            if meta.get("itemprop") == "addressLocality":
                data_dict["city"] = meta["content"]
            if meta.get("itemprop") == "addressRegion":
                data_dict["region"] = meta["content"]
            if meta.get("itemprop") == "addressCountry":
                data_dict["country"] = meta["content"]
