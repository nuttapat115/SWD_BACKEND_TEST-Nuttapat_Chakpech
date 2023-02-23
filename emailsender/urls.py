from django.urls import path
from emailsender import views

urlpatterns = [
    path("", views.EmailSend.as_view(), name='emailsender'), 
]