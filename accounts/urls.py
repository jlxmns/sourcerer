from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('redirect/', views.login_redirect, name='login_redirect'),
]
