from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    path('', views.grimoire_list, name='grimoire_list'),
    path('grimoire/<int:grimoire_id>/', views.grimoire_detail, name='grimoire_detail'),
    path('feitico/<int:spell_id>/', views.spell_detail, name='spell_detail'),
    path('feitico/<int:spell_id>/submeter/', views.spell_submit, name='spell_submit'),
]
