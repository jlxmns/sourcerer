from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.models import StudentProfile, TeacherProfile


@login_required
def dashboard(request):
    user = request.user

    if user.is_teacher():
        teacher_profile = TeacherProfile.objects.get(user=user)
        guilds = teacher_profile.guilds.all()
        return render(
            request,
            'dashboard/teacher.html',
            {
                'teacher_profile': teacher_profile,
                'guilds': guilds,
            }
        )

    student_profile = StudentProfile.objects.get(user=user)
    active_enrollments = student_profile.enrollments.filter(is_active=True).select_related('guild')

    return render(
        request,
        'dashboard/student.html',
        {
            'student_profile': student_profile,
            'active_enrollments': active_enrollments,
        }
    )