from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from accounts.forms import EmailAuthenticationForm
from accounts import views

urlpatterns = [
    path("", views.home, name="home"),
    path("admin/", admin.site.urls),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html",
            authentication_form=EmailAuthenticationForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path(
        "alterar-senha/",
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "senha-alterada/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("accounts/", include("accounts.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("classes/", include("classes.urls")),
    path("content/", include("content.urls")),
    path("students/", include("students.urls")),
    path("notifications/", include("notifications.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
