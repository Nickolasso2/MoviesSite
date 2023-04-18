from dataclasses import fields
from django import forms
from .models import ReviewViaMptt, Rating, RatingStar



class ReviewFormMptt(forms.ModelForm):

    class Meta:
        model = ReviewViaMptt
        fields = ('name', 'email', 'text')
        widgets = {'text':forms.Textarea(attrs={'rows':'5'})}



class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(queryset=RatingStar.objects.all(), widget=forms.RadioSelect)#RadioSelect - input type="radio"

    class Meta:
        model = Rating
        fields = ['star']
        


        
