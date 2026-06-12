from django.contrib.auth.decorators import login_required
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from accounts.models import TeacherProfile, StudentProfile
from classes.models import Guild, GuildMembership, GuildFoeProgress, PowerfulFoe
from content.models import Grimoire, Spell, SpellCompletion, UserBadge


@login_required
def teacher_dashboard(request):
    if not request.user.is_teacher():
        messages.error(request, 'Acesso restrito a professores.')
        return redirect('login')

    teacher = request.user.teacher_profile
    guilds = Guild.objects.filter(head_teacher=teacher)

    context = {
        'teacher': teacher,
        'guilds': guilds,
    }
    return render(request, 'dashboard/teacher_dashboard.html', context)


@login_required
def teacher_create_guild(request):
    if not request.user.is_teacher():
        messages.error(request, 'Acesso restrito a professores.')
        return redirect('login')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if not name:
            messages.error(request, 'O nome da guilda é obrigatório.')
            return redirect('dashboard:teacher_dashboard')

        guild = Guild.objects.create(
            name=name,
            head_teacher=request.user.teacher_profile
        )

        for foe in PowerfulFoe.objects.all():
            GuildFoeProgress.objects.create(guild=guild, foe=foe)

        messages.success(request, f'Guilda "{guild.name}" criada com sucesso!')
        return redirect('dashboard:guild_detail', guild_id=guild.pk)

    return redirect('dashboard:teacher_dashboard')


@login_required
def guild_detail(request, guild_id):
    if not request.user.is_teacher():
        messages.error(request, 'Acesso restrito a professores.')
        return redirect('login')

    guild = get_object_or_404(
        Guild,
        pk=guild_id,
        head_teacher=request.user.teacher_profile
    )

    memberships = GuildMembership.objects.filter(guild=guild).select_related(
        'student__user'
    )

    students_data = []
    for membership in memberships:
        student = membership.student
        total_completions = SpellCompletion.objects.filter(
            student=student
        ).count()
        grimoires_completed = _count_grimoires_completed(student)
        students_data.append({
            'student': student,
            'total_completions': total_completions,
            'grimoires_completed': grimoires_completed,
        })

    context = {
        'guild': guild,
        'students_data': students_data,
        'student_count': guild.student_count(),
    }
    return render(request, 'dashboard/guild_detail.html', context)


def _count_grimoires_completed(student: StudentProfile) -> int:
    count = 0
    for grimoire in Grimoire.objects.all():
        total = grimoire.spells.count()
        if total == 0:
            continue
        completed = SpellCompletion.objects.filter(
            student=student,
            spell__grimoire=grimoire
        ).values('spell').distinct().count()
        if completed >= total:
            count += 1
    return count


def _compute_grimoire_status(student, grimoire):
    total = grimoire.spells.count()
    if total == 0:
        return 'available', 0

    completed = SpellCompletion.objects.filter(
        student=student,
        spell__grimoire=grimoire
    ).values('spell').distinct().count()

    if completed >= total:
        return 'completed', completed
    elif not grimoire.is_unlocked_for(student):
        return 'blocked', completed
    elif completed > 0:
        return 'in_progress', completed
    else:
        return 'available', completed


@login_required
def student_dashboard(request):
    if not request.user.is_student():
        messages.error(request, 'Acesso restrito a alunos.')
        return redirect('login')

    student = request.user.student_profile

    membership = GuildMembership.objects.filter(
        student=student
    ).select_related('guild').first()

    if not membership:
        return redirect('students:no_guild')

    badges = UserBadge.objects.filter(
        student=student
    ).select_related('badge')

    displayed_badges = badges.exclude(display_order__isnull=True).order_by('display_order')

    grimoires = Grimoire.objects.all().prefetch_related('spells')
    grimoires_data = []
    total_grimoires = 0
    completed_grimoires = 0
    pending_spells = 0

    for grimoire in grimoires:
        total = grimoire.spells.count()
        total_grimoires += 1
        status, completed_count = _compute_grimoire_status(student, grimoire)

        if status == 'completed':
            completed_grimoires += 1
        elif status != 'blocked' and total > 0:
            pending_spells += total - completed_count

        earned_xp = 0
        if status != 'blocked' and completed_count > 0:
            spell_xp = SpellCompletion.objects.filter(
                student=student,
                spell__grimoire=grimoire
            ).aggregate(total_xp=models.Sum('spell__mana_reward'))['total_xp'] or 0
            if completed_count >= total:
                spell_xp += grimoire.mana_reward
            earned_xp = spell_xp

        grimoires_data.append({
            'grimoire': grimoire,
            'total': total,
            'completed': completed_count,
            'status': status,
            'progress': int(completed_count / total * 100) if total > 0 else 0,
            'total_xp': grimoire.total_xp(),
            'earned_xp': earned_xp,
            'unlock_requirements': grimoire.unlock_requirements(student) if status == 'blocked' else [],
        })

    ranking = membership.guild.ranking()
    ranking_position = None
    for idx, profile in enumerate(ranking, start=1):
        if profile.pk == student.pk:
            ranking_position = idx
            break

    current_foe = membership.guild.current_foe()

    guild_ranking_data = []
    for idx, profile in enumerate(ranking, start=1):
        guild_ranking_data.append({
            'position': idx,
            'student': profile,
            'is_me': profile.pk == student.pk,
        })

    context = {
        'student': student,
        'avatar_image': student.avatar.get_image_for_level(student.level) if student.avatar else None,
        'membership': membership,
        'badges': displayed_badges,
        'grimoires_data': grimoires_data,
        'ranking_position': ranking_position,
        'current_foe': current_foe,
        'total_grimoires': total_grimoires,
        'completed_grimoires': completed_grimoires,
        'pending_spells': pending_spells,
        'guild_ranking': guild_ranking_data,
        'guild_student_count': membership.guild.student_count(),
    }
    return render(request, 'dashboard/student_dashboard.html', context)
