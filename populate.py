from project.api.planting_status.models import Machines, Plantings, Seedlings


def seedMachine(db):
    db.session.add(Machines(pincode=1234, raspberry_ip='127.0.0.1', currently_backlit=False, currently_irrigating=False, smart_irrigation_enabled=False, smart_illumination_enabled=False, planting_active=False))
    db.session.commit()


def seedPlanting(db):
    machine = Machines.query.first()
    seedling = Seedlings.query.first()
    db.session.add(Plantings(name='fejao', planting_date='2019-10-06 15:43:40.300649', sprouted_seedlings=0, current_humidity=20, current_temperature=30, hours_backlit=5, cycle_finished=True, picture_url='url', machine=machine, seedling=seedling))
    db.session.commit()


def seedSeedlings(db):
    db.session.add(Seedlings(name='fejao', average_harvest_time=20, humidity_threshold=50))
    db.session.commit()
