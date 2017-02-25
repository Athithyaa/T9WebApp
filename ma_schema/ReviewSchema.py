from marshmallow_sqlalchemy import ModelSchema
from models.Review import Review


class ReviewSchema(ModelSchema):
    class Meta:
        model = Review

