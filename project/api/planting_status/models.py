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


    def __init__(self, pincode=None, raspberry_ip=None, currently_backlit=None, currently_irrigating=None, smart_irrigation_enabled=None, smart_illumination_enabled=None, planting_active=None):
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
    # NOTE current_humidity = umidadeSolo
    current_humidity = db.Column(db.Integer)
    current_air_humidity = db.Column(db.Integer)
    current_temperature = db.Column(db.Integer)
    hours_backlit = db.Column(db.String(100))
    cycle_finished = db.Column(db.Boolean)
    cycle_ending_date = db.Column(db.DateTime, default=None)
    picture_url = db.Column(db.String(200))

    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'))
    machine = db.relationship("Machines", back_populates="plantings")

    seedling_id = db.Column(db.Integer, db.ForeignKey('seedlings.id'))
    seedling = db.relationship("Seedlings", back_populates="plantings")

    irrigations_history = db.relationship(
        "IrrigationsHistory", back_populates="planting")
    illuminations_history = db.relationship(
        "IlluminationsHistory", back_populates="planting")


class Seedlings(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(200), nullable=False)
    average_harvest_time = db.Column(db.Integer, nullable=False)
    humidity_threshold = db.Column(db.Integer)

    plantings = db.relationship("Plantings", back_populates="seedling")

class IrrigationSchedules(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    start_time = db.Column(db.DateTime, nullable=False)

    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'))
    machine = db.relationship("Machines", back_populates="irrigation_schedules")


class IrrigationsHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    irrigation_date = db.Column(db.DateTime, nullable=False)
    irrigation_mode = db.Column(db.Integer, nullable=False)

    planting_id = db.Column(db.Integer, db.ForeignKey('plantings.id'))
    planting = db.relationship("Plantings", back_populates="irrigations_history")


class IlluminationSchedules(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'))
    machine = db.relationship("Machines", back_populates="illumination_schedules")


class IlluminationsHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    illumination_start_date = db.Column(db.DateTime, nullable=False)
    illumination_end_date = db.Column(db.DateTime)
    illumination_mode = db.Column(db.Integer, nullable=False)

    planting_id = db.Column(db.Integer, db.ForeignKey('plantings.id'))
    planting = db.relationship("Plantings", back_populates="illuminations_history")
