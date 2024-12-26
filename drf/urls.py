from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf.users import UserViewSet
from drf.messages import MessageViewSet

user_router = DefaultRouter()
user_router.register('', UserViewSet)

message_router = DefaultRouter()
message_router.register('', MessageViewSet)

urlpatterns = [
    path('users/', include(user_router.urls)),
    path('messages/', include(message_router.urls)),
]
