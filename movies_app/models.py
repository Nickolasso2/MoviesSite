from statistics import mean
from datetime import date
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext as _

class Category(models.Model):
    # films by category
    name =models.CharField(max_length=150)
    description = models.TextField()
    url =models.SlugField(max_length=160)

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.url})
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        

class Actor(models.Model):
    # actors 
    name = models.CharField('Name', max_length=100)
    age = models.PositiveSmallIntegerField('Age', default=0)
    image = models.ImageField('Photo', upload_to='actors/')
    description = models.TextField('Description')

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('actor', kwargs={'slug' : self.name})

    class Meta:
        verbose_name = 'Actor'
        verbose_name_plural = 'Actors'

class Genre(models.Model):
    name = models.CharField('Genre', max_length=100)
    description = models.TextField('Description')
    url =models.SlugField(max_length=160, unique=True)

    def get_absolute_url(self):
        return reverse('genre', kwargs={'slug': self.url})

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

class Movie(models.Model):
    title = models.CharField(verbose_name=_('Film title'), max_length=100)#verbose_name=_('Назва фільму') повинно перекладати поля моделі в адмінці але не працює
    description = models.TextField(verbose_name=_('Description'))
    poster = models.ImageField(verbose_name=_('Poster'), upload_to='movies/')
    year = models.PositiveSmallIntegerField(verbose_name=_('Year'))
    country = models.CharField(verbose_name=_('Country'), max_length=30)
    actors = models.ManyToManyField(Actor, verbose_name=_('Actors'), related_name='film_actors')
    genres = models.ManyToManyField(Genre, verbose_name=_('Genres'))
    world_premiere =models.DateField( default=date.today)
    budget = models.PositiveIntegerField(default=0, help_text='dollarUS')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField(default=False)

    def rating(self):
        rating = [rating.value for rating in self.rating_set.all()]
        return mean(rating)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    def get_absolute_url(self):
        return reverse('single_movie',kwargs={'slug':self.url})


class MovieShot(models.Model):
    #кадри з фільму
    title = models.CharField('Назва', max_length=100)
    description = models.TextField('Опис')
    image = models.ImageField('Зображення', upload_to='movie_shots/')
    movie = models.ForeignKey(Movie, verbose_name='Фільм', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Кадр'
        verbose_name_plural = 'Кадри'


class Rating(models.Model):
    ip = models.CharField('Ip', max_length=15)
    value = models.PositiveSmallIntegerField('Star value', default=0)
    # star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='зірка')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Movie')

    def __str__(self) -> str:
        return f'{self.value} - {self.movie}' 

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'


class ReviewViaMptt(MPTTModel):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    text = models.TextField(max_length=5000)
    parent = TreeForeignKey('self', verbose_name='parent', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='film')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.name} - {self.movie}'


    class MPTTMeta:
        order_insertion_by = ['-created_at']
        
    

        









    
    

