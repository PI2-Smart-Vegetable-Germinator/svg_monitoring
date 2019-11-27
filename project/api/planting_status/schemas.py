from project import ma
from project.api.planting_status.models import Plantings, Machines, Seedlings
from marshmallow import fields


class PlantingsSchema(ma.ModelSchema):
    id = fields.Integer(data_key='id')
    name = fields.Str(data_key='name')
    planting_date = fields.DateTime(data_key='planting_date')
    cycle_ending_date = fields.DateTime(data_key='cycle_ending_date')
    cycle_finished = fields.Boolean(data_key='cycle_finished')
    picture_url = fields.Str(data_key='picture_url')
    seedling_id = fields.Integer(data_key='seedling_id')

    class Meta:
        model = Plantings
        fields = ('id', 'name', 'planting_date', 'cycle_ending_date', 'cycle_finished', 'picture_url',
                'seedling_id')


class PlantingInfoSchema(ma.ModelSchema):
    id = fields.Integer(data_key='plantingId')
    current_humidity = fields.Integer(data_key='currentHumidity')
    current_air_humidity = fields.Integer(data_key='currentAirHumidity')
    current_temperature = fields.Integer(data_key='currentTemperature')

    class Meta:
        model = Plantings
        fields = ('id', 'name', 'current_humidity', 'current_temperature', 'current_air_humidity')
