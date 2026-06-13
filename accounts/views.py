from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import StudentRegistrationForm


def register(request):
    if request.user.is_authenticated:
        return redirect("accounts:login_redirect")

    form = StudentRegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user, backend="accounts.auth_backends.EmailAuthBackend")
        messages.success(
            request, "Conta criada com sucesso! Bem-vindo ao Sourcerer."
        )
        return redirect("dashboard:student_dashboard")

    return render(request, "accounts/register.html", {"form": form})


def home(request):
    if request.user.is_authenticated:
        if request.user.is_student():
            return redirect("dashboard:student_dashboard")
        elif request.user.is_teacher():
            return redirect("dashboard:teacher_dashboard")
        return redirect("admin:index")
    return redirect("login")


@login_required
def login_redirect(request):
    if request.user.is_student():
        return redirect("dashboard:student_dashboard")
    elif request.user.is_teacher():
        return redirect("dashboard:teacher_dashboard")
    return redirect("admin:index")
