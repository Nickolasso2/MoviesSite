from django import template
from movies_app.models import Genre, Movie, Category, Rating, RatingStar
from django.db.models import Avg

register = template.Library()

@register.inclusion_tag('movies_app/sidebar.html')
def show_sidebar():
    genres = Genre.objects.all()
    years = [movie.year for movie in Movie.objects.all()]
    years_distinkt = [i for i in set(years)]
    return {'genres':genres, 'years':years_distinkt}

@register.simple_tag()
def categories():
    return  Category.objects.all()

@register.simple_tag()
def genres():
    return  Genre.objects.all()

@register.inclusion_tag('movies_app/star_rating.html')
def rating(movie):
      
    return {'star_rating': movie.rating()}

  

     
    
