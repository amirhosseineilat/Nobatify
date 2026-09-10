from django.test import SimpleTestCase
from django.urls import reverse, resolve

from appointments.views import (
    TimeSlotListView,
    MyAppointmentListView,
    AppointmentBookView,
    AppointmentCancelView,
    AppointmentDetail,
)


class AppointmentURLTest(SimpleTestCase):

    def test_appointment_url(self):
        url = reverse("appointment")

        self.assertEqual(
            url,
            "/appointments/appointment/",
        )

        self.assertEqual(
            resolve(url).func.view_class,
            TimeSlotListView,
        )

    def test_my_appointment_url(self):
        url = reverse("my_appointment")

        self.assertEqual(
            url,
            "/appointments/appointment/my",
        )

        self.assertEqual(
            resolve(url).func.view_class,
            MyAppointmentListView,
        )

    def test_appointment_book_url(self):
        url = reverse(
            "appointment_book",
            kwargs={"pk": 10},
        )

        self.assertEqual(
            url,
            "/appointments/appointment/10/book/",
        )

        self.assertEqual(
            resolve(url).func.view_class,
            AppointmentBookView,
        )

    def test_appointment_cancel_url(self):
        url = reverse(
            "appointment_cancel",
            kwargs={"pk": 10},
        )

        self.assertEqual(
            url,
            "/appointments/appointment/10/cancel/",
        )

        self.assertEqual(
            resolve(url).func.view_class,
            AppointmentCancelView,
        )

    def test_appointment_detail_url(self):
        url = reverse(
            "appointment_detail",
            kwargs={"pk": 10},
        )

        self.assertEqual(
            url,
            "/appointments/appointment/10/detail/",
        )

        self.assertEqual(
            resolve(url).func.view_class,
            AppointmentDetail,
        )

