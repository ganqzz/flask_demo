from dataclasses import dataclass


@dataclass(frozen=True)
class Article:
    id: str
    body: str


@dataclass(frozen=True)
class Articles:
    values: [Article]
