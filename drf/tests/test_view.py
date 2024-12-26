from django.test import TestCase, Client
from django.urls import reverse
from decouple import config
from drf.models import User, Message
import json
from drf.common_methods import create_jwt
import jwt

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
        self.message = Message.objects.create(
            user_id=self.user.id, title='testtiltle', body='testbody'
            )
        self.bearer_token = 'Bearer ' + create_jwt(self.user.email)

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

    def test_drf_message_create(self):
        response = self.client.post(
            reverse('message-list'),
            json.dumps({"title": "testtitle2", "body": "testbody2"}),
            **self.json_request, headers={'Authorization': self.bearer_token}
            )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('title'), 'testtitle2')

    def test_drf_message_create_wrong_date(self):
        self.drf_message_create_invalid_data_invaldi_jwt()
        self.drf_message_create_invalid_data_invaldi_not_exist_user()
        self.drf_message_create_invalid_data_null_mail()
        self.drf_message_create_invalid_data_empty_string_mail()
        self.drf_message_create_invalid_json()
        self.drf_message_create_invalid_empty_title()
        self.drf_message_create_invalid_data_invaldi_without_jwt()

    def drf_message_create_invalid_data_invaldi_jwt(self):
        response = self.client.post(
            reverse('message-list'),
            json.dumps({"title": "testtitle2", "body": "testbody2"}),
            **self.json_request, headers={'Authorization': 'invalidjwt'}
              )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()['detail'], 'invalid jwt.'
            )

    def drf_message_create_invalid_data_invaldi_not_exist_user(self):
        response = self.client.post(
            reverse('message-list'),
            json.dumps({"title": "testtitle2", "body": "testbody2"}),
            **self.json_request,
            headers={
                'Authorization': 'bearer ' + create_jwt('notexsit@test.test')
                }
            )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()['detail'], 'invalid jwt.'
            )

    def drf_message_create_invalid_data_invaldi_without_jwt(self):
        response = self.client.post(
            reverse('message-list'),
            json.dumps({"title": "testtitle2", "body": "testbody2"}),
            **self.json_request
            )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()['detail'], 'invalid jwt.'
            )

    def drf_message_create_invalid_data_null_mail(self):
        response = self.client.post(
            reverse('message-list'),
            json.dumps({"title": "testtitle2", "body": "testbody2"}),
            **self.json_request,
            headers={
                'Authorization': 'bearer ' + create_jwt(None)
                }
            )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()['detail'], 'invalid jwt.'
              )

    def drf_message_create_invalid_data_empty_string_mail(self):
        response = self.client.post(
            reverse('message-list'),
            json.dumps({"title": "testtitle2", "body": "testbody2"}),
            **self.json_request,
            headers={'Authorization': 'bearer ' + create_jwt('')}
            )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()['detail'], 'invalid jwt.'
            )

    def drf_message_create_invalid_data_inccorect_mail(self):
        response = self.client.post(
            reverse('message-list'),
            json.dumps({"title": "testtitle2", "body": "testbody2"}),
            **self.json_request,
            headers={'Authorization': 'bearer ' + create_jwt('asfasfasf')}
              )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()['detail'], 'invalid jwt.'
            )

    def drf_message_create_invalid_json(self):
        response = self.client.post(
            reverse('message-list'),
            json.dumps({"title": "testtitle2", "body": "testbody2"})+'sfsf',
            **self.json_request,
            headers={'Authorization': self.bearer_token}
            )
        self.assertEqual(response.status_code, 400)
        self.assertNotEqual(response.json()['detail'], None)

    def drf_message_create_invalid_empty_title(self):
        response = self.client.post(
            reverse('message-list'),
            json.dumps({"title": "", "body": "testbody2"}),
            **self.json_request,
            headers={'Authorization': self.bearer_token}
            )
        self.assertEqual(response.status_code, 400)
        self.assertNotEqual(
            response.json()['title'], None
              )

    def test_drf_list_messages(self):
        Message.objects.create(
            user_id=self.user.id,
            title='testtiltle2', body='testbody2'
            )
        Message.objects.create(
            user_id=self.user.id,
            title='testtiltle3', body='testbody3'
            )
        response = self.client.get(
            reverse('message-list'),
            headers={'Authorization': self.bearer_token}
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.json()['results']), 3
            )

    def test_drf_list_messages_query_params_search(self):
        Message.objects.create(
            user_id=self.user.id,
            title='testtiltle2', body='testbody2'
            )
        Message.objects.create(
            user_id=self.user.id,
            title='testtiltle3', body='testbody3'
            )
        response = self.client.get(
            reverse('message-list'),
            {'search_by': 'body2'},
            headers={'Authorization': self.bearer_token}
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['results'][1]['body'], 'testbody2'
            )
        self.assertEqual(len(response.json()['results']), 3)

    def test_drf_list_messages_query_params(self):
        Message.objects.create(
            user_id=self.user.id,
            title='testtiltle2',
            body='testbody2'
            )
        Message.objects.create(
            user_id=self.user.id,
            title='testtiltle3', body='testbody3'
            )
        response = self.client.get(
            reverse('message-list'),
            {'limit': '1', 'offset': '0'},
            headers={'Authorization': self.bearer_token}
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 1)

    def test_drf_list_messages_wrong_query(self):
        Message.objects.create(
            user_id=self.user.id,
            title='testtiltle2', body='testbody2'
            )
        Message.objects.create(
            user_id=self.user.id,
            title='testtiltle3', body='testbody3'
            )
        response = self.client.get(
            reverse('message-list'), {'limit': 'sdsd', 'offset': 'dsds'},
            headers={'Authorization': self.bearer_token}
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.json()['results']), 3
            )
        self.assertEqual(
            response.json()['results'][2]['body'], 'testbody3'
            )

    def test_drf_message_detail(self):
        response = self.client.get(
            reverse('message-detail', kwargs={'pk': self.message.id}),
            headers={'Authorization': self.bearer_token}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['title'], 'testtiltle'
        )

    def test_drf_message_detail_wrong_date(self):
        self.drf_message_detail_not_exist_pk()
        self.drf_message_detail_invalid_data_invaldi_jwt()
        self.drf_message_detail_invalid_data_not_exist_mail()
        self.drf_message_detail_invalid_data_null_mail()
        self.drf_message_detail_invalid_data_empty_string_mail()
        self.drf_message_detail_invalid_data_inccorect_mail()

    def drf_message_detail_without_jwt(self):
        response = self.client.get(
            reverse('message-detail', kwargs={'pk': self.message.id})
        )
        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            response.json()['detail'], 'invalid jwt.'
        )

    def drf_message_detail_not_exist_pk(self):
        response = self.client.get(
            reverse('message-detail', kwargs={'pk': 1024}),
            headers={'Authorization': self.bearer_token}
        )
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            response.json()['detail'],
            'No Message matches the given query.'
        )

    def drf_message_detail_invalid_data_invaldi_jwt(self):
        response = self.client.get(
            reverse('message-detail', kwargs={'pk': self.message.id}),
            headers={'Authorization': 'invalidjsfswt'}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()['detail'],
            'invalid jwt.'
        )

    def drf_message_detail_invalid_data_not_exist_mail(self):
        response = self.client.get(
            reverse('message-detail', kwargs={'pk': self.message.id}),
            headers={'Authorization': 'bearer ' + jwt.encode(
                {'email': 'notexsit@test.test'},
                JWT_SECRET_KEY, algorithm="HS256"
            )}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()['detail'], 'invalid jwt.'
        )

    def drf_message_detail_invalid_data_null_mail(self):
        response = self.client.get(
            reverse('message-detail', kwargs={'pk': self.message.id}),
            headers={'Authorization': 'bearer ' + jwt.encode(
                {'email': None}, JWT_SECRET_KEY, algorithm="HS256"
            )}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()['detail'], 'invalid jwt.'
        )

    def drf_message_detail_invalid_data_empty_string_mail(self):
        response = self.client.get(
            reverse('message-detail', kwargs={'pk': self.message.id}),
            headers={'Authorization': 'bearer ' + jwt.encode(
                {'email': ''}, JWT_SECRET_KEY, algorithm="HS256"
            )}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()['detail'], 'invalid jwt.'
        )

    def drf_message_detail_invalid_data_inccorect_mail(self):
        response = self.client.get(
            reverse(
                'message-detail', kwargs={'pk': self.message.id}
            ),
            headers={'Authorization': 'bearer ' + jwt.encode(
                {'email': 'asfasfsaf'}, JWT_SECRET_KEY, algorithm="HS256"
            )}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()['detail'], 'invalid jwt.'
        )

    def test_drf_message_update(self):
        response = self.client.put(
            reverse('message-detail', kwargs={'pk': self.message.id}),
            json.dumps({"title": "updatetitle", "body": "updatebody"}),
            **self.json_request,
            headers={'Authorization': self.bearer_token}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['title'], 'updatetitle'
        )

    def test_drf_message_update_wrong_date(self):
        self.drf_message_update_not_exist_pk()
        self.drf_message_update_invalid_data_invaldi_jwt()
        self.drf_message_update_invalid_data_not_exist_mail()
        self.drf_message_update_invalid_data_null_mail()
        self.drf_message_update_invalid_data_empty_string_mail()
        self.drf_message_update_invalid_data_inccorect_mail()
        self.drf_message_update_invalid_data_null_request()
        self.drf_message_update_invalid_data_null_tittle()
        self.drf_message_update_invalid_data_without_tittle()

    def drf_message_update_without_jwt(self):
        response = self.client.put(
            reverse('message-detail', kwargs={'pk': self.message.id}),
            json.dumps({"title": "updatetitle", "body": "updatebody"}),
            **self.json_request,
            headers={'Authorization': self.bearer_token}
        )
        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            response.json()['detail'], 'invalid jwt.'
        )

    def drf_message_update_not_exist_pk(self):
        response = self.client.put(
            reverse('message-detail', kwargs={'pk': 1024}),
            json.dumps({"title": "updatetitle", "body": "updatebody"}),
            **self.json_request,
            headers={'Authorization': self.bearer_token}
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()['detail'],
            'No Message matches the given query.'
        )

    def drf_message_update_invalid_data_invaldi_jwt(self):
        response = self.client.put(
            reverse('message-detail', kwargs={'pk': self.message.id}),
            json.dumps({"title": "updatetitle", "body": "updatebody"}),
            **self.json_request,
            headers={'Authorization': 'invalidjsfswt'}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()['detail'],
            'invalid jwt.'
        )

    def drf_message_update_invalid_data_not_exist_mail(self):
        response = self.client.put(
            reverse('message-detail', kwargs={'pk': self.message.id}),
            json.dumps({"title": "updatetitle", "body": "updatebody"}),
            **self.json_request,
            headers={'Authorization': 'bearer ' + jwt.encode(
                {'email': 'notexsit@test.test'},
                JWT_SECRET_KEY, algorithm="HS256"
            )}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()['detail'], 'invalid jwt.'
        )

    def drf_message_update_invalid_data_null_mail(self):
        response = self.client.put(
            reverse('message-detail', kwargs={'pk': self.message.id}),
            json.dumps({"title": "updatetitle", "body": "updatebody"}),
            **self.json_request,
            headers={'Authorization': 'bearer ' + jwt.encode(
                {'email': None}, JWT_SECRET_KEY, algorithm="HS256"
            )}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()['detail'], 'invalid jwt.'
        )

    def drf_message_update_invalid_data_empty_string_mail(self):
        response = self.client.put(
            reverse('message-detail', kwargs={'pk': self.message.id}),
            json.dumps({"title": "updatetitle", "body": "updatebody"}),
            **self.json_request,
            headers={'Authorization': 'bearer ' + jwt.encode(
                {'email': ''}, JWT_SECRET_KEY, algorithm="HS256"
            )}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()['detail'], 'invalid jwt.'
        )

    def drf_message_update_invalid_data_inccorect_mail(self):
        response = self.client.put(
            reverse(
                'message-detail', kwargs={'pk': self.message.id}
            ),
            json.dumps({"title": "updatetitle", "body": "updatebody"}),
            **self.json_request,
            headers={'Authorization': 'bearer ' + jwt.encode(
                {'email': 'asfasfsaf'}, JWT_SECRET_KEY, algorithm="HS256"
            )}
        )
        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            response.json()['detail'], 'invalid jwt.'
        )

    def drf_message_update_invalid_data_null_request(self):
        response = self.client.put(
            reverse('message-detail', kwargs={'pk': self.message.id}),
            **self.json_request,
            headers={'Authorization': self.bearer_token}
        )
        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            response.json()['title'], ['This field is required.']
        )

    def drf_message_update_invalid_data_null_tittle(self):
        response = self.client.put(
            reverse('message-detail', kwargs={'pk': self.message.id}),
            json.dumps({"title": "", "body": "updatebody"}),
            **self.json_request,
            headers={'Authorization': self.bearer_token}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['title'], ['This field may not be blank.']
        )

    def drf_message_update_invalid_data_without_tittle(self):
        response = self.client.put(
            reverse('message-detail', kwargs={'pk': self.message.id}),
            json.dumps({"body": "updatebody"}),
            **self.json_request,
            headers={'Authorization': self.bearer_token}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['title'], ['This field is required.']
        )
