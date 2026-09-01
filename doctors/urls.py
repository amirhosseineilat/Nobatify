from django.urls import path
from .views import (
    DoctorListView,
    DoctorDetailView,
    CommentCreateView,
    SearchDoctorView,
)

urlpatterns = [
    path("doctors/", DoctorListView.as_view(), name="doctors"),
    path("doctors/<int:pk>/", DoctorDetailView.as_view(), name="doctor_detail"),
    path("doctors/search/", SearchDoctorView.as_view(), name="doctor_search"),
    path("doctors/<int:doctor_id>/comments/", CommentCreateView.as_view(), name="add_comment"),
]
