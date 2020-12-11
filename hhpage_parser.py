

class HHPageParser():
    def __init__(self):
        self._d_result = None
        self._l_parser = None

    def parse(self, bs_page):

        self._d_result = dict()
        if not bs_page:
            raise ValueError("Нет страницы для парсинга.")

        if self.is_valid(bs_page):
            for parser in self._l_parser:
                parser.parse(bs_page, self._d_result)

        return self._d_result

    def add_parser(self, parser):
        self._l_parser.add(parser)

    def is_valid(self, bs_page):
        for h2 in bs_page.find_all("h2"):
            if h2.get("data-qa") == "bloko-header-2":
                if h2.text == "Вакансия в архиве":
                    return False

        if not bs_page.find("script", attrs={"data-name":"HH/GoogleDfpService"}):
            return False
        return True
