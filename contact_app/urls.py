# path('contact/', include('contact_app.urls'))
from django.urls import path
from .views import contact_def

urlpatterns = [
    
    path('def/', contact_def, name='add_contact2'),
    

   
  

]