from django.test import TestCase
from doctors.forms import CommentForm





class CommentFormTest(TestCase):

    def test_valid_comment_form(self):
        form = CommentForm(
            data ={
                "rating": "3",
                "content": "doctor is good"
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['rating'], '3')
        self.assertEqual(form.cleaned_data['content'], "doctor is good")
        
    def test_invalid_rating(self):
        form = CommentForm(
            data = {
            
                "rating" : "6",
                "content" : "doctor is good"
                
            }
        )
        
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)
        error_message = form.errors['rating'][0]
        self.assertIn('Ensure this value is less than or equal to 5', error_message)
        
    def test_rating_min_value(self):
        form = CommentForm(
            data = {
                
                "rating" : "1",
                "content" : "doctor is bad"
                                
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['rating'], '1')
        
        
        
    def test_rating_max_value(self):
        form = CommentForm(
            data = {
              
                "rating" : "5",
                "content" : "doctor is very good"                
                
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['rating'], '5')
        
    def test_empty_content(self):
    
        form = CommentForm(
            data = {
                "rating" : "3",
                "content" : "   "  
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)  
        error_message = form.errors['content'][0]
        self.assertIn('This field is required', error_message)