from abc import ABCMeta, abstractmethod
from typing import List

from cleana.domain.user import User


class UserRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_all(self, page: int) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def create(self, data: dict) -> User:
        raise NotImplementedError

    @abstractmethod
    def update(self, id: str, data: dict) -> User:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: str):
        raise NotImplementedError
