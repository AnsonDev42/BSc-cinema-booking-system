from django.urls import path

from . import views

urlpatterns = [
    path('accounting', views.accounting, name='accouting'),
    path('accounting/movie/<int:movie_id>/', views.movie_income, name='movie income'),
]
