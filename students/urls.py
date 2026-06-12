from django.urls import path
from . import views

app_name = "students"

urlpatterns = [
    path("sem-guilda/", views.no_guild, name="no_guild"),
    path("perfil/", views.profile_edit, name="profile_edit"),
]
