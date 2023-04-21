from django.urls import path
from .views import *

urlpatterns = [
    path('', MoviesView.as_view()),
    path('movies/<str:slug>/', MovieDetail.as_view(), name='single_movie'),
    path('category/<str:slug>/', CategoryMovieList.as_view(), name='category'),
     path('genre/<str:slug>/', GenreMovieList.as_view(), name='genre'),
    path('add_comment_mptt/<int:pk>/', AddReviewMptt.as_view(), name='add_comment_mptt'),
    path('movie/actor/<str:slug>/', ActorDetail.as_view(), name='actor'),
    path('filter/', FilterMovie.as_view(), name='filter'),
    path('ajax_filter/', FilterMovieAjax.as_view(), name='filter_ajax'),
    # path('xhr_request/', XhrRequest.as_view(), name='xhr_request'),
    path('rating/',rating, name='rating'),
    path('search/', SearchView.as_view(), name='search'),
    path('set_lang/', SetLang.as_view(), name='set_lang'),

]