from django.urls import path

urlpatterns = [
    path("appointment/", name="appointment"),
    path("appointment/book/", name="appointment_book"),
    path("appointment/cancel/", name="appointment_cancel"),
    path("appointment/<int:pk>/detail/", name="appointment_detail"),
]
