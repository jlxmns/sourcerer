from django.urls import path
from . import views

app_name = 'classes'

urlpatterns = [
    path('entrar/', views.join_guild, name='join_guild'),
    path('guilda/<int:guild_id>/ranking/', views.guild_ranking, name='guild_ranking'),
    path('guilda/<int:guild_id>/inimigo/', views.guild_foe, name='guild_foe'),
]
