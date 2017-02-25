from marshmallow_sqlalchemy import ModelSchema
from models.Company import Company


class CompanySchema(ModelSchema):
    class Meta:
        model = Company

