from django.test import SimpleTestCase
from django.urls import reverse, resolve
from drf.users import UserViewSet
from drf.messages import MessageViewSet


class UrlTest(SimpleTestCase):
    def test_users_drfs_url_user_list(self):
        url = reverse('user-list')
        self.assertEqual(resolve(url).func.cls, UserViewSet)

    def test_users_drfs_url_user_detail(self):
        url = reverse('user-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, UserViewSet)

    def test_messages_drfs_url_user_list(self):
        url = reverse('message-list')
        self.assertEqual(resolve(url).func.cls, MessageViewSet)

    def test_messages_drfs_url_user_detail(self):
        url = reverse('message-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, MessageViewSet)
