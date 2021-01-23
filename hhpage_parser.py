
class HHPageParser():
    def __init__(self):
        self._result = None
        self._parsers = None

    def parse(self, bs_page):
        """
        Метод для парсинга страницы вакансии всеми
        зарегестрированными парсерами.
        """
        self._result = dict()
        # Проверяем наличие страницы для парсинга
        if not bs_page:
            raise ValueError("Нет страницы для парсинга.")

        # Запускаем все парсеры по очереди
        if self.is_valid(bs_page):
            for parser in self._parsers:
                parser.parse(bs_page, self._result)

        return self._result

    def add_parser(self, parser):
        """
        Метод для добавления парсера
        """
        self._parsers.add(parser)

    def is_valid(self, bs_page):
        """
        Метод проверки страницы на валидность. Если страница отличается от
        стандартной или находиться в архиве, то возвращаем false
        """
        for h2 in bs_page.find_all("h2"):
            if h2.get("data-qa") == "bloko-header-2":
                if h2.text == "Вакансия в архиве":
                    return False

        if not bs_page.find("script", attrs={"data-name":"HH/GoogleDfpService"}):
            return False
        return True
