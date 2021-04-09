from abc import ABCMeta, abstractmethod


class ArticleUsecase(metaclass=ABCMeta):
    @abstractmethod
    def get_list(self, page: int = None, per_page: int = None) -> dict:
        raise NotImplementedError

    @abstractmethod
    def retrieve(self, id: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    def create(self, data: dict) -> dict:
        raise NotImplementedError

    @abstractmethod
    def update(self, id: str, data: dict) -> dict:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: str):
        raise NotImplementedError
