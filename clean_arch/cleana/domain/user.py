from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: int
    username: str
    password: str
    email: str
