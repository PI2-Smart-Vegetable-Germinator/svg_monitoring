from datetime import datetime

from project.tests.base import BaseTestCase
from project import db
from project.api.planting_status.models import Machines
from project.api.planting_status.models import IrrigationsHistory
from project.api.planting_status.models import Plantings


class IrrigationTest(BaseTestCase):
    def create_machine(self):
        machine = Machines(planting_active=True)
        db.session.add(machine)
        db.session.commit()

        return machine

    def create_planting(self):
        machine = self.create_machine()
        planting = Plantings(
            name='Tomate',
            planting_date=datetime.today(),
            sprouted_seedlings=0,
            current_humidity=20,
            current_temperature=30,
            hours_backlit=5,
            cycle_finished=False,
            picture_url='url',
            machine=machine
        )
        db.session.add(planting)
        db.session.commit()

        return planting
        

    def test_irrigation_starts_with_correct_data_and_no_conflict(self):
        planting = self.create_planting()

        with self.client:
            response = self.client.post('/api/start_irrigation', json={'plantingId': planting.id})
            history = IrrigationsHistory.query.all()

            self.assertEqual(response.status_code, 201)
            self.assertEqual(len(history), 1)
            self.assertEqual(planting.machine.currently_irrigating, True)

    def test_irrigation_fails_if_irrigation_already_on(self):
        planting = self.create_planting()
        planting.machine.currently_irrigating = True
        db.session.add(planting)
        db.session.commit()

        with self.client:
            response = self.client.post('/api/start_irrigation', json={'plantingId': planting.id})

            self.assert403(response)

    def test_end_irrigation_ends_an_irrigation_correctly(self):
        planting = self.create_planting()
        with self.client:
            start_response = self.client.post('/api/start_irrigation', json={'plantingId': planting.id})
            end_response = self.client.post('/api/end_irrigation', json={'plantingId': planting.id})

            self.assertEqual(end_response.status_code, 201)
            self.assertEqual(planting.machine.currently_irrigating, False)
