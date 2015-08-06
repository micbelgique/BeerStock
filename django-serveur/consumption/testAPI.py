from tastypie.test import ResourceTestCase
from .models import Record, User
import random
import string


def randomword(length):
    """ Get a random world """
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


def randomid(length):
    """ Get a random id """
    return ''.join(random.choice(string.hexdigits) for i in range(length))


class RecordTest(ResourceTestCase):
    def get_random_record(self, with_pulse=True):
        data = {
            'rfid_uid_0': 0,
            'rfid_uid_1': 0,
            'rfid_uid_2': 0,
            'rfid_uid_3': random.randint(1, 5),
        }
        if(with_pulse):
            data['pulse'] = random.randint(1, 30)
        else:
            data['quantity'] = random.random() * 250
        return data

    def test_post_new_record(self):
        """ Add a new record with the API"""
        self.assertEqual(Record.objects.count(), 0)
        self.assertHttpCreated(
            self.api_client.post(
                '/api/v1/record_rfid/', format='json',
                data=self.get_random_record()))
        # Verify a new one has been added.
        self.assertEqual(Record.objects.count(), 1)
        self.assertHttpCreated(
            self.api_client.post(
                '/api/v1/record_rfid/', format='json',
                data=self.get_random_record(False)))
        self.assertEqual(Record.objects.count(), 2)


class UserTest(ResourceTestCase):
    def get_new_user(self):
        return {
            'facebook_id': randomid(50),
            'first_name': randomword(50),
            'last_name': randomword(50),
        }

    def test_post_new_user_json(self):
        """ Add a new user its facebook_id with application/json header"""
        new_user = self.get_new_user()
        self.assertEqual(User.objects.count(), 0)
        self.assertHttpCreated(
            self.api_client.post(
                '/api/v1/user/', format='json', data=new_user))
        self.assertEqual(User.objects.count(), 1)
        self.assertHttpCreated(
            self.api_client.post(
                '/api/v1/user/', format='json', data=new_user))
        self.assertEqual(User.objects.count(), 1)
