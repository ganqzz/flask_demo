from cleana.repository.user.user_repository import UserRepository
from cleana.usecase.auth.auth_usecase import AuthUseCase


class AuthInteractor(AuthUseCase):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def login(self, body: str):
        pass

    def logout(self):
        pass

    def sign_up(self, body: str):
        pass

    def update(self, body: str):
        pass
