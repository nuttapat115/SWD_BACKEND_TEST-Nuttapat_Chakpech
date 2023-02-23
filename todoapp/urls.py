from django.urls import path
from todoapp import views

urlpatterns = [

    path("task/", views.CreateTaskAPIView.as_view(), name='taskcreate'),
    path("task/<int:id>", views.TaskAPIView.as_view(), name='taskedit'),

]