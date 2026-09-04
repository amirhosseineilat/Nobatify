from django import forms
from .models import Comment,Doctor, Speciality

class CommentForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,  
        label="Rating"
    )

    class Meta:
        model = Comment
        fields = ['rating', 'content']
        
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),  
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
                    "placeholder": "نام پزشک",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "admin-input",
                    "placeholder": "نام خانوادگی پزشک",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "admin-input",
                    "placeholder": "doctor@example.com",
                    "dir": "ltr",
                }
            ),
            "specialities": forms.CheckboxSelectMultiple(
                attrs={
                    "class": "admin-specialities",
                }
            ),
        }