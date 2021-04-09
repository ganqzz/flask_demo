from unittest import TestCase

from cleana.domain.article import Article, Articles
from cleana.repository.article.memory_article_repository import MemoryArticleRepository


class TestArticleRepository(TestCase):
    def test_get(self):
        repository = MemoryArticleRepository()

        self.assertEqual(
            Articles(values=[Article(id="1", body="test")]),
            repository.get_list(1)
        )
