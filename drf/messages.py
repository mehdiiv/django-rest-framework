from rest_framework.viewsets import GenericViewSet
from drf.users import LimitOffsetPagination
from drf.models import Message
from drf.serializers import MessageSerializer
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin,
    RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin)
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from drf.common_methods import authorization, AuthorizeError
from rest_framework.filters import SearchFilter


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        try:
            user = authorization(token)
            return (user, None)
        except AuthorizeError:
            raise AuthenticationFailed('invalid jwt.')


class MessageViewSet(
    CreateModelMixin, ListModelMixin,
    UpdateModelMixin, RetrieveModelMixin,
    DestroyModelMixin, GenericViewSet
     ):
    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(user=user)

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = LimitOffsetPagination
    authentication_classes = [JWTAuthentication]
    filter_backends = [SearchFilter]
    search_fields = ['title', 'body']
