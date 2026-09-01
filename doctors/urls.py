from django.urls import path
from .views import *

urlpatterns = [
    path("doctors/", DoctorListView.as_view(), name="doctors"),
    path("doctors/<int:pk>/detail", DoctorDetailView.as_view(), name="doctor_detail"),
    path("search/", SearchDoctorView.as_view(), name="search"),
]
