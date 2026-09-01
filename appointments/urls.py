from django.urls import path
from .views import *

urlpatterns = [
    path("appointment/", AppointmentListView.as_view(), name="appointment"),
    path("appointment/my", MyAppointmentListView.as_view(), name="my_appointment"),
    path("appointment/<int:pk>/book/", AppointmentBookView.as_view(), name="appointment_book"),
    path(
        "appointment/<int:pk>/cancel/",
        AppointmentCancelView.as_view(),
        name="appointment_cancel",
    ),
    path(
        "appointment/<int:pk>/detail/",
        AppointmentDetail.as_view(),
        name="appointment_detail",
    ),
]
