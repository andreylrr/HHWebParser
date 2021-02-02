import parsers.basic_parser as bp

"""
    Class Experience parses html page to extract the data which 
    related to the required experience for the open position
"""


class ExperienceParser(bp.BaseParser):
    def parse(self, html_page, data_dict):
        s_experience = None
        for span in html_page.find_all("span"):
            if span.get("data-qa") == "vacancy-experience":
                s_experience = span.text
                break
        if s_experience :
            if s_experience == "не требуется":
                data_dict["experience"] = "0"
            elif s_experience.startswith("более"):
                data_dict["experience"] = s_experience.split(" ")[1]
            elif s_experience.startswith("от"):
                data_dict["experience"] = s_experience.split(" ")[1]
            else:
                l_exp_split = s_experience.split(" ")
                l_exp_split = l_exp_split[0].split("–")

                for s_exp in l_exp_split:
                    if s_exp.isdigit():
                        data_dict["experience"] = s_exp
                        break
