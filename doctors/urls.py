from django.urls import path

urlpatterns = [
    path("doctors/", name="doctors"),
    path("doctors/<int:pk>/detail", name="doctor_detail"),
]
