from abc import ABCMeta, abstractmethod


class AuthUseCase(metaclass=ABCMeta):
    @abstractmethod
    def login(self, body: str):
        raise NotImplementedError

    @abstractmethod
    def logout(self):
        raise NotImplementedError

    @abstractmethod
    def sign_up(self, body: str):
        raise NotImplementedError

    @abstractmethod
    def update(self, body: str):
        raise NotImplementedError
