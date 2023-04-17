from django.shortcuts import render, redirect
from contact_app.forms import ContactForm
from django.views.generic import CreateView
from django.http import JsonResponse
from .models import Contact
    
def contact_def(request):
    if request.method =='POST':
        email = request.POST['email']
        form = ContactForm(request.POST)
        if form.is_valid():
            if Contact.objects.filter(email=email).exists():
                return JsonResponse({'result':f'You had already signed up with {email}', 'hide':'true'}, status=200)
            else:
                form.save()            
            return JsonResponse({'result':'You\'ve succesfully signed up. Cool!', 'hide':'true'}, status=200)
        else:
            return JsonResponse({'result':'Validation error'}, status=200)

