from django import forms

from .models import TimeSlot


class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = [
            "doctor",
            "date",
            "start_time",
            "end_time",
        ]

        widgets = {
            "doctor": forms.Select(
                attrs={
                    "class": "admin-input",
                }
            ),
            "date": forms.DateInput(
                attrs={
                    "class": "admin-input",
                    "type": "date",
                }
            ),
            "start_time": forms.TimeInput(
                attrs={
                    "class": "admin-input",
                    "type": "time",
                }
            ),
            "end_time": forms.TimeInput(
                attrs={
                    "class": "admin-input",
                    "type": "time",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError(
                "ساعت پایان باید بعد از ساعت شروع باشد."
            )

        return cleaned_data