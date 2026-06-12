from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path("listar/", views.list_notifications, name="list"),
    path("ler/<int:notification_id>/", views.mark_read, name="mark_read"),
]
