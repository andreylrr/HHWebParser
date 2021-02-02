import parsers.basic_parser as bp

"""
    Class KeySkills parses html page to extract the data which 
    related to key skills required for this position
"""


class KeySkillsParser(bp.BaseParser):
    def parse(self, html_page, data_dict):
        l_skills = []
        for div_element in html_page.find_all("div", attrs={"data-qa":"bloko-tag bloko-tag_inline skills-element"}):
            l_skills.append(div_element.contents[0].text)
        data_dict["skills"] = l_skills
