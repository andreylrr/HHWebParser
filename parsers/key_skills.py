import parsers.basic_parser as bp

"""
    Class KeySkills parses html page to extract the data which 
    related to key skills required for this position
"""


class KeySkills(bp.BaseParser):
    def parse(self, html_page, data_dict):
        l_skills = []
        for span in html_page.find_all("span"):
            if span.get("data-qa") == "skills-element":
                l_skills.append(span.get("data-tag-id"))
        data_dict["skills"] = l_skills
