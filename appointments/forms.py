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
            "price",
        ]

        widgets = {

            "doctor": forms.Select(
                attrs={
                    "class": "slot-input",
                }
            ),

            "date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "class": "slot-input",
                    "type": "hidden",
                }
            ),

            "start_time": forms.TimeInput(
                format="%H:%M",
                attrs={
                    "class": "slot-input",
                }
            ),

            "end_time": forms.TimeInput(
                format="%H:%M",
                attrs={
                    "class": "slot-input",
                }
            ),

            "price": forms.NumberInput(
                attrs={
                    "class": "slot-input",
                    "placeholder": "مثلاً 500000",
                    "min": "0",
                    "step": "1000",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time:

            if start_time >= end_time:

                raise forms.ValidationError(
                    "ساعت پایان باید بعد از ساعت شروع باشد."
                )

        return cleaned_data