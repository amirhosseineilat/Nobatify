from django import forms
from .models import Comment


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