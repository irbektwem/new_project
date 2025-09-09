from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit/', views.submit_quote, name='submit_quote'),
    path('like/<int:quote_id>/', views.like_quote, name='like_quote'),
    path('dislike/<int:quote_id>/', views.dislike_quote, name='dislike_quote'),
]