from abc import ABCMeta, abstractmethod

from cleana.domain.article import Article, Articles


class ArticleRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_list(self, page: int) -> Articles:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: str) -> Article:
        raise NotImplementedError

    @abstractmethod
    def create(self, data: dict) -> Article:
        raise NotImplementedError

    @abstractmethod
    def update(self, id: str, data: dict) -> Article:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: str):
        raise NotImplementedError
