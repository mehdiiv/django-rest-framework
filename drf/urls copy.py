from django.urls import path
from api.users import UsersView
from api.messages import MessagesViews, MessageView

urlpatterns = [
    path('users/', UsersView.as_view(), name='users'),
    path('messages/', MessagesViews.as_view(), name='messages'),
    path('messages/<int:pk>/', MessageView.as_view(), name='message'),

]
