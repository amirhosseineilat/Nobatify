from appointments.forms import TimeSlotForm
from django.test import TestCase


class TimeSlotFormTest(TestCase):
    def test_valid_form(self):
        data = {
            "doctor": "ali",
            "date": "2024-06-15",
            "start_time": "10:00",
            "end_time": "11:00",
            "price": 100,
        }

        form = TimeSlotForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            "doctor": "ali",
            "date": "2024-06-15",
            "start_time": "10:00",
            "end_time": "11:00",
            "price": -100,
        }

        form = TimeSlotForm(data=data)
        self.assertFalse(form.is_valid())

    def test_missing_fields(self):
        data = {
            "doctor": "ali",
            "date": "2024-06-15",
            "start_time": "10:00",
            "end_time": "11:00",
        }

        form = TimeSlotForm(data=data)
        self.assertFalse(form.is_valid())

    def test_clean_method(self):
        data = {
            "doctor": "ali",
            "date": "2024-06-15",
            "start_time": "10:00",
            "end_time": "11:00",
            "price": 100,
        }

        form = TimeSlotForm(data=data)
        self.assertTrue(form.is_valid())
        cleaned_data = form.clean()
        self.assertEqual(cleaned_data["doctor"], "ali")
        self.assertEqual(cleaned_data["date"], "2024-06-15")
        self.assertEqual(cleaned_data["start_time"], "10:00")
        self.assertEqual(cleaned_data["end_time"], "11:00")
        self.assertEqual(cleaned_data["price"], 100)
