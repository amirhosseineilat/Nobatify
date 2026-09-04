from django import forms
from .models import Comment,Doctor, Speciality

class CommentForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(
            attrs={
                'class': 'hidden'
            }
        ),
        label="Rating"
    )

    class Meta:
        model = Comment
        fields = ['rating', 'content']

        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'class': (
                    'w-full rounded-2xl border-2 border-[#E8D6C8] '
                    'bg-white p-4 text-[#1D4533] outline-none '
                    'transition focus:border-[#1D4533]'
                ),
                'placeholder': 'تجربه خود را درباره این پزشک بنویسید...'
            }),
        }

        labels = {
            'content': 'Review',
        }


class SpecialityForm(forms.ModelForm):
    class Meta:
        model = Speciality
        fields = ["name"]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "admin-input",
                    "placeholder": "مثلاً قلب و عروق",
                }
            ),
        }


# class DoctorForm(forms.ModelForm):
#     class Meta:
#         model = Doctor
#         fields = [
#             "first_name",
#             "last_name",
#             "email",
#             "specialities",
#         ]

#         widgets = {
#             "first_name": forms.TextInput(
#                 attrs={
#                     "class": "admin-input",
#                     "placeholder": "نام پزشک",
#                 }
#             ),
#             "last_name": forms.TextInput(
#                 attrs={
#                     "class": "admin-input",
#                     "placeholder": "نام خانوادگی پزشک",
#                 }
#             ),
#             "email": forms.EmailInput(
#                 attrs={
#                     "class": "admin-input",
#                     "placeholder": "doctor@example.com",
#                     "dir": "ltr",
#                 }
#             ),
#             "specialities": forms.CheckboxSelectMultiple(
#                 attrs={
#                     "class": "admin-specialities",
#                 }
#             ),
#         }
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            "first_name",
            "last_name",
            "email",
            "specialities",
        ]

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "admin-input",
                    "placeholder": "مثلاً علی",
                    "autocomplete": "given-name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "admin-input",
                    "placeholder": "مثلاً احمدی",
                    "autocomplete": "family-name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "admin-input",
                    "placeholder": "doctor@example.com",
                    "dir": "ltr",
                    "autocomplete": "email",
                }
            ),
            "specialities": forms.CheckboxSelectMultiple(
                attrs={
                    "class": "admin-specialities",
                }
            ),
        }