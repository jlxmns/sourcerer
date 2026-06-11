from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from .models import SchoolClass, Enrollment
from accounts.models import TeacherProfile, StudentProfile


@login_required
def create_guild(request):
    """Professor cria uma nova guilda (turma)."""
    if not request.user.is_teacher():
        return redirect('dashboard')

    teacher = TeacherProfile.objects.get(user=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')

        if not name:
            return redirect('create_guild')

        SchoolClass.objects.create(teacher=teacher, name=name, description=description)
        return redirect('dashboard')

    return render(request, 'classes/create_guild.html')


@login_required
def join_guild(request):
    """Aluno entra em uma guilda via código de convite."""
    if not request.user.is_student():
        return redirect('dashboard')

    student = StudentProfile.objects.get(user=request.user)

    if request.method == 'POST':
        invite_code = request.POST.get('invite_code', '').strip().upper()

        if not invite_code:
            return redirect('dashboard')

        try:
            guild = SchoolClass.objects.get(invite_code=invite_code)
        except ObjectDoesNotExist:
            # Código inválido
            return redirect('dashboard')

        # Verifica se já está matriculado
        if Enrollment.objects.filter(student=student, guild=guild, is_active=True).exists():
            return redirect('dashboard')

        Enrollment.objects.create(student=student, guild=guild)
        return redirect('dashboard')

    return redirect('dashboard')
