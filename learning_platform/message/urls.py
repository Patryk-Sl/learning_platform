from django.urls import path
from .views import MessageListView, MessageCreateView, MessageDetailView, MessageDeleteView


urlpatterns = [

    path('message/', MessageListView.as_view(), name='index'),
    path('message/new/', MessageCreateView.as_view(), name='message_new'),
    path('message/<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('message/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),

]
