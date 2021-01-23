from abc import ABC, abstractmethod


class BaseWriter(ABC):
    """
        Абстрактный класс для классов сохранения данных,
        которые были получены в результате парсинга web страниц
    """
    @abstractmethod
    async def write(self, data):
        print("Writing in Base class")

    @abstractmethod
    def close(self):
        print("Cleaning after you")