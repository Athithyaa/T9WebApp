from marshmallow_sqlalchemy import ModelSchema
from models.User import User


class UserSchema(ModelSchema):
    class Meta:
        model = User

