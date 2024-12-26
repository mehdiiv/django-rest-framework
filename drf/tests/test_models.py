from django.test import TestCase
from decouple import config
from drf.models import User, Message
from drf.common_methods import create_jwt

JWT_SECRET_KEY = config('JWT_SECRET_KEY')


class UserModelTest(TestCase):
    def setUp(self):
        self.jwt_code = create_jwt('test@test.com')
        self.user = User.objects.create(
            email='test@test.com', json_web_token=create_jwt('test@test.com')
        )
        self.user = User.objects.create(
            email='test@test.com', json_web_token=self.jwt_code
        )
        self.message = Message.objects.create(
            user_id=self.user.id, title='testtiltle', body='testbody'
        )

    def test_model_user_cerate(self):
        self.assertEqual(self.user.email, 'test@test.com')
        self.assertEqual(self.user.json_web_token, create_jwt('test@test.com'))

    def test_user_table_name(self):
        self.assertEqual(self.user._meta.db_table, 'users')

    def test_model_message_create(self):
        self.assertEqual(self.message.title, 'testtiltle')
        self.assertEqual(self.message.body, 'testbody')

    def test_message_table_name(self):
        self.assertEqual(self.message._meta.db_table, 'messages')
