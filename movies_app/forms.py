from dataclasses import fields
from django import forms
from .models import ReviewViaMptt, Rating



class ReviewFormMptt(forms.ModelForm):

    class Meta:
        model = ReviewViaMptt
        fields = ('name', 'email', 'text')
        widgets = {'text':forms.Textarea(attrs={'rows':'5'})}


# adding rating
class RatingForm(forms.ModelForm):
    choices = [
        (5,'5'),
        (4,'4'),
        (3,'3'),
        (2,'2'),
        (1,'1'),
    ]
    star = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)#RadioSelect - input type="radio"

    class Meta:
        model = Rating
        fields = ['star']
        


        
