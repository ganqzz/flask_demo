from cleana.domain.article import Articles, Article
from cleana.repository.article.article_repository import ArticleRepository

# In-memory
DB = [
    {"id": "1", "body": "Hoge Hoge"},
    {"id": "2", "body": "Fuga Fuga"},
    {"id": "3", "body": "Awaaaaa!!"},
]
hwm = len(DB) + 1


class MemoryArticleRepository(ArticleRepository):
    def get_list(self, page: int) -> Articles:
        return Articles([Article(**a) for a in DB])

    def get_by_id(self, id: str) -> Article:
        data = self.find_first(id)
        return Article(**data)

    def create(self, data: dict) -> Article:
        global hwm
        data.update(id=str(hwm))
        # uniqueなど、DB関連のValidationは必要
        DB.append(data)
        hwm += 1
        return Article(**data)

    def update(self, id: str, data: dict) -> Article:
        target_data = self.find_first(id)
        target_data.update(data)
        return Article(**target_data)

    def delete(self, id: str):
        DB.remove(self.find_first(id))

    def find_first(self, id: str) -> dict:
        try:
            # find first
            data: dict = next(filter(lambda a: a["id"] == id, DB))
        except StopIteration:
            raise ValueError('Not Found') from None

        return data
