from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.teacher_dashboard, name='teacher_dashboard'),
    path('aluno/', views.student_dashboard, name='student_dashboard'),
    path('criar-guilda/', views.guild_form, name='create_guild'),
    path('guilda/<int:guild_id>/', views.guild_detail, name='guild_detail'),
    path('guilda/<int:guild_id>/editar/', views.guild_form, name='edit_guild'),
    path('progresso/', views.teacher_progress, name='teacher_progress'),
    path('alertas/', views.teacher_alerts, name='teacher_alerts'),
]
