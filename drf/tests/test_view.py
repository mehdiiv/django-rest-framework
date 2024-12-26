from django.test import TestCase, Client
from django.urls import reverse
from decouple import config
from drf.models import User
import json
from drf.common_methods import create_jwt

JWT_SECRET_KEY = config('JWT_SECRET_KEY')


class DrfTest(TestCase):
    def setUp(self):
        create_jwt(email='test@test.com')
        self.user = User.objects.create(
            email='test@test.com',
            json_web_token=create_jwt('test@test.com')
        )
        self.client = Client()
        self.json_request = {'content_type': 'application/json'}

    def test_drf_user_create(self):
        response = self.client.post(
            reverse('user-list'),
            json.dumps({"email": "test@test1.com"}),
            **self.json_request
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('email'), 'test@test1.com')

    def test_drf_user_create_invalid_data_invalid_json(self):
        response = self.client.post(
            reverse('user-list'),
            json.dumps({"email": "test@test1.com"}) + 'sd',
            **self.json_request
        )
        self.assertEqual(response.status_code, 400)
        self.assertNotEqual(response.json()['detail'], None)

    def test_drf_user_create_wrong_date(self):
        self.drf_user_create_invalid_data_null_mail()
        self.drf_user_create_invalid_data_exist_empty_srting()
        self.drf_user_create_invalid_data_inccorect_mail()

    def drf_user_create_invalid_data_null_mail(self):
        response = self.client.post(
            reverse('user-list'),
            json.dumps({"email": None}),
            **self.json_request
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['email'],
            ['This field may not be null.']
        )

    def drf_user_create_invalid_data_exist_empty_srting(self):
        response = self.client.post(
            reverse('user-list'),
            json.dumps({"email": ''}),
            **self.json_request
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['email'],
            ['This field may not be blank.']
        )

    def drf_user_create_invalid_data_inccorect_mail(self):
        response = self.client.post(
            reverse('user-list'),
            json.dumps({"email": 'test@test'}),
            **self.json_request
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['email'],
            ['Enter a valid email address.']
        )

    def test_drf_users_list_limit(self):
        User.objects.create(
            email='test3@test3.com',
            json_web_token=create_jwt('test3@test3.com')
            )
        User.objects.create(
            email='test2@test2.com',
            json_web_token=create_jwt('test2@test2.com')
              )
        response = self.client.get(
            reverse('user-list'),
            {'limit': 2, 'offset': '0'}
              )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.json()['results']), 2
            )

    def test_drf_users_list_invalid_limit(self):
        User.objects.create(
            email='test3@test3.com',
            json_web_token=create_jwt('test3@test3.com')
        )
        User.objects.create(
            email='test2@test2.com',
            json_web_token=create_jwt('test2@test2.com')
        )
        response = self.client.get(
            reverse('user-list'),
            {'limit': 'sfsafa',  'offset': 'sdsd'}
         )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.json()['results']), 3
            )

    def test_drf_user_detail(self):
        response = self.client.get(
            reverse('user-detail', kwargs={'pk': self.user.id}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['email'],
            'test@test.com'
        )

    def test_drf_user_detail_invalid_pk(self):
        response = self.client.get(
            reverse('user-detail', kwargs={'pk': self.user.id + 20}),
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()['detail'],
            'No User matches the given query.'
        )

    def test_drf_user_update(self):
        response = self.client.post(
            reverse('user-detail', kwargs={'pk': self.user.id}),
            {'email': 'update@gmail.com'}
        )
        self.assertEqual(response.status_code, 405)
