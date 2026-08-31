from django.urls import path
from .views import *

urlpatterns = [
    path("appointment/", AppointmentListView.as_view(), name="appointment"),
    path("appointment/book/", AppointmentBookView.as_view(), name="appointment_book"),
    path(
        "appointment/cancel/",
        AppointmentCancelView.as_view(),
        name="appointment_cancel",
    ),
    path(
        "appointment/<int:pk>/detail/",
        AppointmentDetail.as_view(),
        name="appointment_detail",
    ),
]
