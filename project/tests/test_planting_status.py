from project.tests.base import BaseTestCase
from project.api.planting_status.models import Machines, Plantings, Seedlings
import json
from project import db
import datetime
from project.tests.utils import add_machine, add_planting, add_seedling


class PlantingStatusTest(BaseTestCase):
    def test_ping(self):
        response = self.client.get('/api/ping')
        self.assert200(response)


class PlantingTimeStatus(BaseTestCase):
    def test_get_planting_time(self):

        current_date = datetime.datetime.today()

        db.session.add(Machines(pincode=1234, raspberry_ip='192.168.1.8', currently_backlit=False, currently_irrigating=False, smart_irrigation_enabled=False, smart_illumination_enabled=False, planting_active=False))
        db.session.commit()
        db.session.add(Plantings(name='Tomate', planting_date=current_date, sprouted_seedlings=0,current_humidity=20, current_temperature=30, hours_backlit=5, cycle_finished=True, picture_url='url'))
        db.session.commit()

        with self.client:
            response = self.client.get('/api/planting-time')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(0, data['data']['planting_time'])
            self.assertIn('Tomate', data['data']['planting_name'])
