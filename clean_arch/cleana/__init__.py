from flask import Flask

from cleana.controller.article_resource import ArticleResource
from cleana.repository.article.memory_article_repository import MemoryArticleRepository
from cleana.usecase.article.article_interactor import ArticleInteractor


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config)

    # Dependency Injection
    article_repository = MemoryArticleRepository()
    article_usecase = ArticleInteractor(article_repository)
    article_resource = ArticleResource(article_usecase)

    # register routes
    article_resource.register_routes(app)

    return app
