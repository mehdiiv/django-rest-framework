from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin)
from .serializers import UserSerializer
from drf.models import User


class LimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5
    default_offset = 0
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 50


class UserViewSet(
        CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet
        ):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
