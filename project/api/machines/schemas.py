from project import ma
from project.api.planting_status.models import Machines
from marshmallow import fields


class CreateMachineSchema(ma.ModelSchema):
    pincode = fields.Str(required=True)

    class Meta:
        model = Machines


class UpdateMachineSchema(ma.ModelSchema):
    id = fields.Integer(required=True)
    class Meta:
        model = Machines
