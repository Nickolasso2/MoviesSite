from django import forms
from .models import Contact
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError

class ContactForm(forms.ModelForm):
    captcha = CaptchaField()
    
    class Meta:
        model = Contact
        fields= ['email']
        widgets = {
            'email':forms.EmailInput(attrs={'id':'form5Example21'}),'captcha':forms.TextInput(attrs={'class':'form-control'})
        }