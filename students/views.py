from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from accounts.models import Avatar, StudentProfile
from content.models import UserBadge


@login_required
def no_guild(request):
    if not request.user.is_student():
        messages.error(request, "Acesso restrito a alunos.")
        return redirect("login")

    student = request.user.student_profile
    return render(request, "students/no_guild.html", {"student": student})


@login_required
def profile_edit(request):
    if not request.user.is_student():
        messages.error(request, "Acesso restrito a alunos.")
        return redirect("login")

    student = request.user.student_profile
    avatars = Avatar.objects.all()

    all_badges = UserBadge.objects.filter(
        student=student
    ).select_related("badge").order_by("-created_at")

    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        avatar_id = request.POST.get("avatar")
        badge_slots = {
            1: request.POST.get("badge_slot_1"),
            2: request.POST.get("badge_slot_2"),
            3: request.POST.get("badge_slot_3"),
        }

        if first_name:
            request.user.first_name = first_name
            request.user.save()

        if avatar_id:
            avatar = get_object_or_404(Avatar, pk=avatar_id)
            student.avatar = avatar
            student.save()

        for ub in all_badges:
            ub.display_order = None
            ub.save()

        for slot, badge_id in badge_slots.items():
            if badge_id:
                try:
                    ub = all_badges.get(pk=badge_id)
                    ub.display_order = slot
                    ub.save()
                except UserBadge.DoesNotExist:
                    pass

        messages.success(request, "Perfil atualizado com sucesso!")
        return redirect("students:profile_edit")

    context = {
        "student": student,
        "avatars": avatars,
        "all_badges": all_badges,
    }
    return render(request, "students/profile_edit.html", context)
