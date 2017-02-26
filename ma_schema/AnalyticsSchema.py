from marshmallow_sqlalchemy import ModelSchema
from models.Analytics import Analytics


class AnalyticsSchema(ModelSchema):
    class Meta:
        model = Analytics