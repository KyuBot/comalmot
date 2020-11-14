from django.urls import path, include
from . import views

app_name = 'Mecab'

urlpatterns = [
    path('', views.word),
]
