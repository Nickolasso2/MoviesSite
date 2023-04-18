from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import Actor, Category, Movie, Genre, Rating
from django.views.generic import DetailView, ListView
from .forms import ReviewFormMptt, RatingForm
from django.http import HttpResponseNotFound, JsonResponse, HttpResponse
from django.db.models import Q
from django.core import serializers
from django.core.paginator import Paginator


def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class GenreYear:

    def get_genres(self):
        return Genre.objects.all()

    def get_year(self):
        return Movie.objects.filter(draft=False).values('year')


class MoviesView(GenreYear, ListView):
    model = Movie
    paginate_by=3
    template_name= 'movies_app/collected.html'

    # def get_queryset(self):
    #     return Movie.objects.all().prefetch_related('genres').select_related('category')

class CategoryMovieList(MoviesView):
    def get_queryset(self):
        return Movie.objects.filter(category__url=self.kwargs['slug'])

class  GenreMovieList(MoviesView):
    def get_queryset(self):
        return Movie.objects.filter(genres__url=self.kwargs['slug'])

    
class MovieDetail(DetailView):
    model = Movie
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['form'] = ReviewForm()
        context['form_mptt'] = ReviewFormMptt()
        context['categories'] = Category.objects.all()
        context['no_parent_review'] = self.object.reviewviamptt_set.filter(parent__isnull=True)  # passes review_set(query) with no parents
        context['star_form'] = RatingForm()
        
        
        try:
            star_given = Rating.objects.get(ip=get_client_ip(self.request), movie=self.object).star.value
            # якщо get() не знаходить екземпляр моделі, то видає помилку 
            print('star_given:', star_given)
            context['star_given'] = star_given
        except:
            context['star_given'] = 0
            
        return context
    
    


class AddReviewMptt(View):
    

    def post(self, request, pk):
        print('request.POST :', request.POST)
        form = ReviewFormMptt(request.POST)
        if form.is_valid():
            review_object = form.save(commit=False)
            if request.POST.get('parent'):
                review_object.parent_id = int(request.POST.get('parent'))
            review_object.movie_id = pk
            review_object.save()
            row_format = "%d/%m/%Y %H:%M:%S"
            return JsonResponse({
                'status':"success",
                'parent_review_id': request.POST.get('parent'),
                'new_review_id': review_object.pk,
                'name':request.POST.get('name'),
                'text':request.POST.get('text'),
                'created_at':review_object.created_at.strftime(row_format)
                })
        
        else:
            return JsonResponse({'valid':'Помилка валідації!'})
        # return redirect(request.META.get('HTTP_REFERER'))

    def get(self, request, pk):
        return HttpResponseNotFound('There is no such page!!!')

 
class ActorDetail(DetailView):
    model = Actor
    template_name = 'movies_app/actor.html'
    slug_field = 'name'


class FilterMovie(ListView):
    # searching according to filter
    template_name = 'movies_app/collected.html'
    paginate_by = 5

    def get_queryset(self):
        if self.request.GET.getlist('genre') and self.request.GET.getlist('year'):
            queryset = Movie.objects.filter(year__in=self.request.GET.getlist(
                'year'),genres__in=self.request.GET.getlist('genre'))

        else:
            queryset = Movie.objects.filter(Q(year__in=self.request.GET.getlist(
                'year')) | Q(genres__in=self.request.GET.getlist('genre')))

        # queryset = Movie.objects.filter(Q(year__in=self.request.GET.getlist('year')) |  Q(genres__in=self.request.GET.getlist('genre')))

        # print(queryset)# [<Movie: Список Шиндлера>]>
        # print(values)# [{'title': 'Список Шиндлера'}]>

        return queryset.distinct()

# для роботи пагінації при пошуку по чекбоксах--
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['years'] = ''.join([f'year={year}&' for year in self.request.GET.getlist('year')])
        context['genres'] = ''.join([f'genre={genre}&' for genre in self.request.GET.getlist('genre')])
        return context


class FilterMovieAjax(FilterMovie, ListView):
    # father class Filtermovie added to use get_queryset method
   
    def get(self, request):
        html = ''
        
        
        for movie in self.get_queryset():
            print('116', list(movie.genres.all()))
            genres = ''
            
            for genre in movie.genres.all():
                genres += '<span class="money editContent">' + genre.name + '</span><br>'
            html += '<div class="col-md-4 product-men">\
            <div class="product-shoe-info editContent text-center mt-lg-4">\
                <div class="men-thumb-item">\
                    <img src="' + f'{movie.poster.url}' + '" class="img-fluid" alt="">\
                </div>\
                <div class="item-info-product">\
                    <h4 class="">\
                        <a href="' + str(movie.get_absolute_url()) + '" class="editContent">' + movie.title + '</a>\
                    </h4>\
                    <div class="product_price">\
                        <div class="grid-price">\
                            <span class="money editContent">' + movie.tagline+'</span>\
                        </div>\
                    </div>\
                    <div class="product_price">\
                        <div class="grid-price">' + genres + '</div>\
                    </div>\
                    <div class="product_price">\
                        <div class="grid-price">\
                            <span class="money editContent">' + movie.country + '</span>\
                        </div>\
                    </div>\
                    <div class="product_price">\
                        <div class="grid-price">\
                            <span class="money editContent">' + str(movie.year) + '</span>\
                        </div>\
                    </div>\
                    <div class="product_price">\
                        тут має бути фктори через цикл\
                        <div class="grid-price">\
                            <a class="money editContent" href="{{actor.get_absolute_url}}">{{ actor }}</a>\
                        </div>\
                        {% endfor %}\
                    </div>\
                    <div class="product_price">\
                        <div class="grid-price">\
                            <span class="money editContent">' + movie.description + '</span>\
                        </div>\
                    </div>\
                    <ul class="stars">\
                        <li><a href="#"><span class="fa fa-star" aria-hidden="true"></span></a>\
                        </li>\
                        <li><a href="#"><span class="fa fa-star" aria-hidden="true"></span></a>\
                        </li>\
                        <li><a href="#"><span class="fa fa-star-half-o" aria-hidden="true"></span></a>\
                        </li>\
                        <li><a href="#"><span class="fa fa-star-half-o" aria-hidden="true"></span></a>\
                        </li>\
                        <li><a href="#"><span class="fa fa-star-o" aria-hidden="true"></span></a>\
                        </li>\
                    </ul>\
                </div>\
                </div>\
        </div>'

        return JsonResponse({'movies': html})


# testing xhr-requests
class XhrRequest(View):
    def get(self, request):
        movie = Movie.objects.get(pk=2)
        movie_for_xhr_request = serializers.serialize('json', [movie])
        movie_genres = Movie.objects.values('genres', 'id')
        print(movie_genres)
        return JsonResponse({'movie_for_xhr_request': movie_for_xhr_request, 'movie_gen': list(movie_genres)})


def rating(request):
    ip = get_client_ip(request)
    form = RatingForm(request.POST)
    
    if form.is_valid():
        Rating.objects.update_or_create(ip=ip, movie_id=int(request.POST.get("movie")), defaults={'star_id': int(request.POST.get("star"))})
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=400)
        
# the same as rating def only by class
class AddStarRating(View):
    """Добавление рейтинга фильму"""
    

    def post(self, request):
        ip = get_client_ip(request)
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class SearchView(ListView):
    template_name= 'movies_app/collected.html'
    paginate_by = 2

    def get_queryset(self):
        
        return Movie.objects.filter(title__icontains=self.request.GET.get('looking_for', ''))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['looking_for'] = f"looking_for={self.request.GET.get('looking_for')}&"
        return context


class SetLang(View):

    def get(self, request):
        current_url = request.GET.get("current_url")#/de/movies/django-free/
        current_url_cut = current_url[3:]
        language = request.GET.get("language")
        new_url = '/' + language + current_url_cut
        return redirect(new_url)

        
    

