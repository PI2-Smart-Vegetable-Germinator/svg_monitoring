from project import db

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
