from django.contrib import admin
from .models import *
from mptt.admin import MPTTModelAdmin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from modeltranslation.admin import TranslationAdmin

class CategoryAdmin(TranslationAdmin):
    prepopulated_fields = {'url':('name',)}

# class ReviewInline(admin.TabularInline):#to display in a separate object the objects of the model associated with it
#     model = Review # the model to be displayed
#     extra= 1 #number exta empty fields

class MovieAdminEditable(forms.ModelForm):
    description_pl = forms.CharField(widget=CKEditorUploadingWidget())
    description_de = forms.CharField(widget=CKEditorUploadingWidget())
    description_en = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'

    
class MovieAdmin(TranslationAdmin):
    list_display = ['title', 'get_poster', 'draft']
    # inlines = [ReviewInline] # points out the class with the model to display
    save_on_top = True
    save_as = True
    # fields = (('title', 'tagline'),)
    readonly_fields = ['get_poster']
    fieldsets = (
        ('Група 1', {'classes' : ('collapse',),
            'fields' : (('title', 'tagline'),)}),
        ('Група 2', {'fields' : (('poster', 'get_poster'), 'description', 'year', 'country', 'director', 'actors', 'genres', 'world_premiere', 'budget', 'fees_in_usa', 'category', 'url', 'draft')}),
        )
    form = MovieAdminEditable
    
    def get_poster(self, object):
        return mark_safe(f'<img src={object.poster.url} width=100 height=120>')

    def unpublish(self, request, queryset):
        queryset.update(draft=True)

    unpublish.short_description = 'До чорновиків'
    unpublish.allowed_permissions = ('change',)
    actions = ['unpublish']

class ActorAdmin(TranslationAdmin):
    list_display = ('name', 'get_photo')
    readonly_fields = ['get_photo']
    
    def get_photo(self, object):
        return mark_safe(f'<img src={object.image.url} width=100 height=120>')


admin.site.register(Movie, MovieAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Genre)
admin.site.register(MovieShot)
admin.site.register(Rating)
admin.site.register(ReviewViaMptt, MPTTModelAdmin)


