from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .users import UserViewSet

user_router = DefaultRouter()
user_router.register('', UserViewSet)

urlpatterns = [
    path('users/', include(user_router.urls)),
]
