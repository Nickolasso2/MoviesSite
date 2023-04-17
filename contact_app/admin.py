from django.contrib import admin
from contact_app.models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'data')

admin.site.register(Contact, ContactAdmin)

