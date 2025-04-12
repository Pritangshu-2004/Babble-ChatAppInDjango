from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/', views.chatRoom, name="chat"),
    path('<str:username>/get_messages/', views.get_messages, name="get_messages"),
    path('delete_message/<int:message_id>/', views.delete_message, name="delete_message"),  # Ensure this is correct
     path('delete_chat/<str:username>/', views.delete_chat, name="delete_chat"),
]