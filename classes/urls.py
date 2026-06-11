from django.urls import path
from . import views

urlpatterns = [
    path('create-guild/', views.create_guild, name='create_guild'),
    path('join-guild/', views.join_guild, name='join_guild'),
]