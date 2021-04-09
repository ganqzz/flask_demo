from dataclasses import asdict

from cleana.domain.article import Article, Articles
from cleana.repository.article.article_repository import ArticleRepository
from cleana.usecase.article.article_usecase import ArticleUsecase


class ArticleInteractor(ArticleUsecase):
    def __init__(self, article_repository: ArticleRepository):
        self.article_repository = article_repository

    def get_list(self, page: int = None, per_page: int = None) -> dict:
        articles: Articles = self.article_repository.get_list(page)
        return articles_response(articles)

    def retrieve(self, id: str) -> dict:
        article: Article = self.article_repository.get_by_id(id)
        return asdict(article) if article else None

    def create(self, data: dict) -> dict:
        validated_data = validate_data(data)
        article: Article = self.article_repository.create(validated_data)
        return asdict(article)

    def update(self, id: str, data: dict) -> dict:
        validated_data = validate_data(data)
        article: Article = self.article_repository.update(id, validated_data)
        return asdict(article)

    def delete(self, id: str):
        self.article_repository.delete(id)


def validate_data(data: dict) -> dict:
    try:
        # validation (format, fields)
        validated_data: dict = data
    except ValueError:
        raise  # ValidationError

    return validated_data


def articles_response(articles: Articles) -> dict:
    """ translation """
    return {"items": [asdict(article) for article in articles.values]}
