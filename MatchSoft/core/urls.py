from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.start_game, name='start'),
    path('jugar/', views.game_view, name='game'),
    path('responder/', views.submit_answer, name='submit_answer'),
    path('comodin/<str:kind>/', views.use_lifeline, name='lifeline'),
    path('resultado/', views.result_view, name='result'),
]
