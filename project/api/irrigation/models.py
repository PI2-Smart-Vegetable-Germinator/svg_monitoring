from project import db


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
