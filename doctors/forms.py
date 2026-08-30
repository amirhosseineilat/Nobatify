from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['rating','content']

        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Write your review of the visit'
                }
            ),
        }