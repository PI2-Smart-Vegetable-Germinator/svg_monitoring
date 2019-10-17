from project.api.planting_status.models import Machines, Plantings, Seedlings


def seedMachine(db):
    db.session.add(Machines(pincode=1234, raspberry_ip='127.0.0.1', currently_backlit=False, currently_irrigating=False, smart_irrigation_enabled=False, smart_illumination_enabled=False, planting_active=False))
    db.session.commit()


def seedPlanting(db):
    machine = Machines.query.first()
    seedling = Seedlings.query.first()
    db.session.add(Plantings(name='Alface', planting_date='2019-09-29 09:26:03.478039', sprouted_seedlings=0, current_humidity=20, current_temperature=30, hours_backlit=5, cycle_finished=False, picture_url='url', machine=machine, seedling=seedling))
    
    db.session.add(Plantings(name='Alface', planting_date='2019-07-15 15:26:03.478039', sprouted_seedlings=0, current_humidity=25, current_temperature=32, hours_backlit=3, cycle_finished=True, cycle_ending_date='2018-07-31 10:00:03.478039', picture_url='url', machine=machine, seedling=seedling))
    db.session.commit()

    seedling2 = Seedlings.query.order_by(Seedlings.id.desc()).first()
    db.session.add(Plantings(name='Cebolinha', planting_date='2019-05-02 15:26:03.478039', sprouted_seedlings=0, current_humidity=30, current_temperature=28, hours_backlit=0, cycle_finished=True, cycle_ending_date='2019-06-15 10:00:03.478039', picture_url='url', machine=machine, seedling=seedling2))
    db.session.commit()

    db.session.add(Plantings(name='Alface', planting_date='2018-05-19 15:26:03.478039', sprouted_seedlings=0, current_humidity=20, current_temperature=30, hours_backlit=5, cycle_finished=True, cycle_ending_date='2018-06-10 10:00:03.478039', picture_url='url', machine=machine, seedling=seedling))
    db.session.commit()


def seedSeedlings(db):
    db.session.add(Seedlings(name='Alface', average_harvest_time=25, humidity_threshold=40))
    db.session.commit()
    db.session.add(Seedlings(name='Cebolinha', average_harvest_time=45, humidity_threshold=40))
    db.session.commit()
