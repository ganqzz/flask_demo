from unittest import TestCase
from unittest.mock import Mock

from cleana.domain.article import Articles, Article
from cleana.repository.article.article_repository import ArticleRepository
from cleana.usecase.article.article_interactor import ArticleInteractor


class TestArticleInteractor(TestCase):
    def test_get(self):
        repo = Mock(ArticleRepository)
        repo.get_list.return_value = Articles(
            values=[Article(id="1", body="test")]
        )
        usecase = ArticleInteractor(article_repository=repo)

        self.assertEqual({"items": [{"id": "1", "body": "test"}]},
                         usecase.get_list(0))
        repo.get_list.assert_called_with(0)
