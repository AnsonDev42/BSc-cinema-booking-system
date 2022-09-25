from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movie/<int:movie_id>/', views.movie, name='movie'),
    path('movie/choose_your_seat/<int:showtime_id>/', views.seat, name='seat'),
]
