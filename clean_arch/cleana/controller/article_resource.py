from flask import jsonify, request
from flask.views import MethodView

from cleana.usecase.article.article_usecase import ArticleUsecase


class ArticleResource(MethodView):
    def __init__(self, article_usecase: ArticleUsecase):
        self.article_usecase = article_usecase

    def get(self, id: str = None):
        if id:
            try:
                data: dict = self.article_usecase.retrieve(id)
            except Exception:
                return 'Not Found', 404
        else:
            # query param: page, per_page
            data: dict = self.article_usecase.get_list(0)

        return jsonify(data)

    def post(self):
        data: dict = self.article_usecase.create(request.get_json())
        # 401, 403, 400
        return jsonify(data), 201

    def put(self, id: str):
        data: dict = self.article_usecase.update(id, request.get_json())
        # 401, 404, 403, 400
        return jsonify(data), 200

    def delete(self, id: str):
        self.article_usecase.delete(id)
        # 401, 404, 403
        return '', 204

    def register_routes(self, app):
        # id: string
        app.add_url_rule('/', view_func=self.get, methods=['GET'])
        app.add_url_rule('/<id>', view_func=self.get, methods=['GET'])
        app.add_url_rule('/', view_func=self.post, methods=['POST'])
        app.add_url_rule('/<id>', view_func=self.put, methods=['PUT', 'PATCH'])
        app.add_url_rule('/<id>', view_func=self.delete, methods=['DELETE'])
