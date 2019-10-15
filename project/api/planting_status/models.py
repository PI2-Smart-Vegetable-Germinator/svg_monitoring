from project import db
import datetime


class Machines(db.Model):
    __tablename__ = 'machines'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    pincode = db.Column(db.Integer)
    raspberry_ip = db.Column(db.String(30))
    currently_backlit = db.Column(db.Boolean, default=False)
    currently_irrigating = db.Column(db.Boolean, default=False)
    smart_irrigation_enabled = db.Column(db.Boolean, default=False)
    smart_illumination_enabled = db.Column(db.Boolean, default=False)
    planting_active = db.Column(db.Boolean, default=False)

    plantings = db.relationship("Plantings", back_populates="machine")
    irrigation_schedules = db.relationship(
        "IrrigationSchedules", back_populates="machine")
    illumination_schedules = db.relationship(
        "IlluminationSchedules", back_populates="machine")

    def __init__(self, pincode, raspberry_ip, currently_backlit, currently_irrigating, smart_irrigation_enabled, smart_illumination_enabled, planting_active):
        self.pincode = pincode
        self.raspberry_ip = raspberry_ip
        self.currently_backlit = currently_backlit
        self.currently_irrigating = currently_irrigating
        self.smart_irrigation_enabled = smart_irrigation_enabled
        self.smart_illumination_enabled = smart_illumination_enabled
        self.planting_active = planting_active


class Plantings(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(200), nullable=False)
    planting_date = db.Column(db.DateTime)
    sprouted_seedlings = db.Column(db.Integer)
    current_humidity = db.Column(db.Integer)
    current_temperature = db.Column(db.Integer)
    hours_backlit = db.Column(db.Integer)
    cycle_finished = db.Column(db.Boolean)
    cycle_ending_date = db.Column(db.DateTime)
    picture_url = db.Column(db.String(200))

    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'))
    machine = db.relationship("Machines", back_populates="plantings")

    seedling_id = db.Column(db.Integer, db.ForeignKey('seedlings.id'))
    seedling = db.relationship("Seedlings", back_populates="plantings")

    irrigations_history = db.relationship(
        "IrrigationsHistory", back_populates="planting")
    illuminations_history = db.relationship(
        "IlluminationsHistory", back_populates="planting")

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'planting_date': self.planting_date,
            'cycle_ending_date': self.cycle_ending_date,
            'cycle_finished': self.cycle_finished,
            'picture_url': self.picture_url,
            'seedling_id': self.seedling_id
        }


class Seedlings(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(200), nullable=False)
    average_harvest_time = db.Column(db.Integer, nullable=False)
    humidity_threshold = db.Column(db.Integer)

    plantings = db.relationship("Plantings", back_populates="seedling")
