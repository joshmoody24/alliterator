from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit/', views.submit, name='submit'),
    path('results/<str:word1>/<str:word2>/', views.results, name='results'),
    path('error/<str:message>/', views.error, name="error"),
    path('about/', views.about, name='about'),
    path('alliterator/', views.alliterator, name='alliterator'),
]
