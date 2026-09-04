from django.urls import path
from .views import AdminDashboardView
from .views import (
    AdminDoctorListView,
    AdminCreateDoctorView,
    AdminDoctorDetailView,
    AdminDoctorUpdateView,
    AdminDoctorDeleteView,
    AdminSearchDoctor,
    #timeslot
    AdminListTimesLotView,
    AdminCreateTimesLotView,
    AdminUpdaterTimeslotView,
    AdminTimesLotDeleteView,
    AdminTimeSlotSearchView
)

urlpatterns = [
    path('', AdminDashboardView.as_view(), name='admin_dashboard'),
    path(
        "admin_doctors/",
        AdminDoctorListView.as_view(),
        name="admin_doctor_list",
    ),

    path(
        "admin_doctor_create/",
        AdminCreateDoctorView.as_view(),
        name="admin_doctor_create",
    ),

    path(
        "admin_doctor_detail/<int:pk>/",
        AdminDoctorDetailView.as_view(),
        name="admin_doctor_detail",
    ),

    path(
        "admin_doctor_update/<int:pk>/",
        AdminDoctorUpdateView.as_view(),
        name="admin_doctor_update",
    ),

    path(
        "admin_doctor_delete/<int:pk>/",
        AdminDoctorDeleteView.as_view(),
        name="admin_doctor_delete",
    ),
    path("search/",AdminSearchDoctor.as_view(),name="admin_doctor_search"),
    path("admin_timeslots/",AdminListTimesLotView.as_view(),name="admin_timeslots"),
    path("admin_timeslots_create/",AdminCreateTimesLotView.as_view(),name="admin_timeslot_create"),
    path("admin_timeslot_update/<int:pk>/",AdminUpdaterTimeslotView.as_view(),name="admin_timeslot_update"),
    path("admin_timeslot_delete/<int:pk>/",AdminTimesLotDeleteView.as_view(),name="admin_timeslot_delete"),
    path("admin_timeslot_search/",AdminTimeSlotSearchView.as_view(),name="admin_timeslot_search")
]