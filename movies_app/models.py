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
    name = models.CharField('Ім\'я', max_length=100)
    age = models.PositiveSmallIntegerField('Вік', default=0)
    image = models.ImageField('Зображення', upload_to='actors/')
    description = models.TextField('Опис')

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('actor', kwargs={'slug' : self.name})

    class Meta:
        verbose_name = 'Актор'
        verbose_name_plural = 'Актори'

class Genre(models.Model):
    name = models.CharField('Назва', max_length=100)
    description = models.TextField('Опис')
    url =models.SlugField(max_length=160, unique=True)

    def get_absolute_url(self):
        return reverse('genre', kwargs={'slug': self.url})

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанри'

class Movie(models.Model):
    title = models.CharField(verbose_name=_('Назва фільму'), max_length=100)#verbose_name=_('Назва фільму') повинно перекладати поля моделі в адмінці але не працює
    tagline = models.CharField(verbose_name=_('Слоган'), max_length=100, default='')
    description = models.TextField(verbose_name=_('Опис'))
    poster = models.ImageField(verbose_name=_('Постер'), upload_to='movies/')
    year = models.PositiveSmallIntegerField(verbose_name=_('Рік'))
    country = models.CharField(verbose_name=_('Країна'), max_length=30)
    director = models.ManyToManyField(Actor, verbose_name=_('Режисер'), related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name=_('Актори'), related_name='film_actors')
    genres = models.ManyToManyField(Genre, verbose_name=_('Жанри'))
    world_premiere =models.DateField( default=date.today)
    budget = models.PositiveIntegerField(default=0, help_text='вказати суму в доларах США')
    fees_in_usa = models.PositiveIntegerField('Fees', default=0, help_text='вказати суму в доларах США')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField(default=False)

    def rating(self):
        rating = [rating.star.value for rating in self.rating_set.all()]
        return mean(rating)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Фільм'
        verbose_name_plural = 'Фільми'

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


# class RatingStar(models.Model):
#     value = models.PositiveSmallIntegerField('Значення', default=0)

#     def __str__(self) -> str:
#         return f'{self.value}'

#     class Meta:
#         verbose_name = 'Зірка рейтингу'
#         verbose_name_plural = 'Зірки рейтингу'
#         ordering = ['-value']

class Rating(models.Model):
    ip = models.CharField('ip адреса', max_length=15)
    value = models.PositiveSmallIntegerField('Значення', default=0)
    # star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='зірка')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='фільм')

    def __str__(self) -> str:
        return f'{self.value} - {self.movie}' 

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class ReviewViaMptt(MPTTModel):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    text = models.TextField(max_length=5000)
    parent = TreeForeignKey('self', verbose_name='батько', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='фільм')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.name} - {self.movie}'


    class MPTTMeta:
        order_insertion_by = ['-created_at']
        
    

        









    
    

