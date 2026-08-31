from django.urls import path
from .views import *



urlpatterns = [
    path("doctors/",ListView.as_view(), name="doctors"),
    path("doctors/<int:pk>/detail",DetailView.as_view(), name="doctor_detail"),
]
