from project import db
from project.api.planting_status.models import Machines, Plantings, Seedlings


def add_machine(pincode, raspberry_ip, currently_backlit, currently_irrigating, smart_irrigation_enabled, smart_illumination_enabled, planting_active):
    machine = Machines(pincode, raspberry_ip, currently_backlit, currently_irrigating,
                       smart_irrigation_enabled, smart_illumination_enabled, planting_active)
    db.session.add(machine)
    db.session.commit()
    return machine


def add_planting(name, planting_date, sprouted_seedlings, current_humidity, current_temperature, hours_backlit, cycle_finished, picture_url):
    planting = Plantings(name, planting_date, sprouted_seedlings, current_humidity,
                         current_temperature, hours_backlit, cycle_finished, picture_url)
    db.session.add(planting)
    db.session.commit()
    return planting


def add_seedling(name, average_harvest_time, humidity_threshold):
    seedling = Seedlings(name, average_harvest_time, humidity_threshold)
    db.session.add(seedling)
    db.session.commit()
    return seedling
