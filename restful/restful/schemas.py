from . import ma
from .models import Movie, User


# 基本的には、AutoSchemaを使用するより、カスタマイズのし易さも含めて個別フィールドで明示する方が良い
class MovieSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Movie
        include_relationships = True


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True


movie_schema = MovieSchema()
user_schema = UserSchema()
