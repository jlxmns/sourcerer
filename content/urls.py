from django.urls import path
from . import views

urlpatterns = [
    path('modules/', views.module_list, name='module_list'),
    path('modules/<slug:slug>/', views.module_detail, name='module_detail'),
    path('modules/<slug:module_slug>/challenges/<int:challenge_id>/', views.challenge_detail, name='challenge_detail'),
    path('challenges/<int:challenge_id>/save-attempt/', views.save_attempt, name='save_attempt'),
]