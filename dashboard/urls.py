from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.teacher_dashboard, name='teacher_dashboard'),
    path('aluno/', views.student_dashboard, name='student_dashboard'),
    path('criar-guilda/', views.teacher_create_guild, name='create_guild'),
    path('guilda/<int:guild_id>/', views.guild_detail, name='guild_detail'),
]
