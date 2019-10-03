from project.api.planting_status.models import Machines, Plantings, Seedlings


def seedMachine(db):
    db.session.add(Machines(pincode=1234, raspberry_ip='192.168.1.8', currently_backlit=False, currently_irrigating=False, smart_irrigation_enabled=False, smart_illumination_enabled=False, planting_active=False))
    db.session.commit()


def seedPlanting(db):
    db.session.add(Plantings(name='alface', planting_date='2019-09-29 09:26:03.478039', sprouted_seedlings=0, current_humidity=20, current_temperature=30, hours_backlit=5, cycle_finished=False, picture_url='url'))
    db.session.add(Plantings(name='Tomate', planting_date='2018-05-19 15:26:03.478039', sprouted_seedlings=0, current_humidity=20, current_temperature=30, hours_backlit=5, cycle_finished=True, picture_url='url'))
    db.session.commit()


def seedSeedlings(db):
    db.session.add(Seedlings(name='alface', average_harvest_time=25, humidity_threshold=40))
    db.session.commit()
