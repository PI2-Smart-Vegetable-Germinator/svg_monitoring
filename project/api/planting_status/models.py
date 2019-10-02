from project import db


class Machines(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    pincode = db.Column(db.Integer)
    raspberry_ip = db.Column(db.String(30))
    currently_backlit = db.Column(db.Boolean, default=False)
    currently_irrigating = db.Column(db.Boolean, default=False)
    smart_irrigation_enabled = db.Column(db.Boolean, default=False)
    smart_illumination_enabled = db.Column(db.Boolean, default=False)
    planting_active = db.Column(db.Boolean, default=False)

    plantings = db.relationship("Plantings", back_populates="machine")
    irrigation_schedules = db.relationship("IrrigationSchedules", back_populates="machine")
    illumination_schedules = db.relationship("IlluminationSchedules", back_populates="machine")


class Plantings(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(200), nullable=False)
    planting_date = db.Column(db.DateTime)
    sprouted_seedlings = db.Column(db.Integer)
    current_humidity = db.Column(db.Integer)
    current_temperature = db.Column(db.Integer)
    hours_backlit = db.Column(db.Integer)
    cycle_finished = db.Column(db.Boolean)
    picture_url = db.Column(db.String(200))

    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'))
    machine = db.relationship("Machines", back_populates="plantings")

    seedling_id = db.Column(db.Integer, db.ForeignKey('seedlings.id'))
    seedling = db.relationship("Seedlings", back_populates="plantings")

    irrigations_history = db.relationship("IrrigationsHistory", back_populates="planting")
    illuminations_history = db.relationship("IlluminationsHistory", back_populates="planting")


class Seedlings(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(200), nullable=False)
    average_harvest_time = db.Column(db.Integer, nullable=False)
    humidity_threshold = db.Column(db.Integer)

    plantings = db.relationship("Plantings", back_populates="seedling")