from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Max, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
import json

from accounts.models import TeacherProfile, StudentProfile
from classes.models import Guild, GuildMembership, GuildFoeProgress, PowerfulFoe
from content.models import Grimoire, Spell, SpellCompletion, UserBadge


@login_required
def teacher_dashboard(request):
    if not request.user.is_teacher():
        messages.error(request, 'Acesso restrito a professores.')
        return redirect('login')

    teacher = request.user.teacher_profile

    guilds = Guild.objects.filter(
        models.Q(head_teacher=teacher) | models.Q(teachers=teacher),
        is_active=True,
    ).distinct()

    all_students = StudentProfile.objects.filter(
        guild_memberships__guild__in=guilds
    ).distinct()

    total_grimoires = Grimoire.objects.count()

    active_students = all_students.count()
    guild_count = guilds.count()

    completed_spells = SpellCompletion.objects.filter(
        student__in=all_students
    ).count()

    completed_grimoires_count = sum(
        1 for s in all_students if _count_grimoires_completed(s) >= total_grimoires
    )

    earned_badges = UserBadge.objects.filter(
        student__in=all_students
    ).count()

    metrics = {
        'active_students': active_students,
        'guild_count': guild_count,
        'completed_grimoires': completed_grimoires_count,
        'completed_spells': completed_spells,
        'earned_badges': earned_badges,
    }

    guilds_data = []
    for guild in guilds:
        memberships = GuildMembership.objects.filter(guild=guild).select_related('student')
        students_in_guild = [m.student for m in memberships]
        count = len(students_in_guild)

        if count == 0:
            guilds_data.append({
                'guild': guild,
                'student_count': 0,
                'average_level': 0,
                'total_mana': 0,
                'completed_grimoires': 0,
                'completed_spells': 0,
                'progress': 0,
            })
            continue

        total_mana = sum(s.mana for s in students_in_guild)
        avg_level = sum(s.level for s in students_in_guild) / count
        guild_spells = SpellCompletion.objects.filter(
            student__in=students_in_guild
        ).count()
        guild_grimoires = sum(
            1 for s in students_in_guild if _count_grimoires_completed(s) >= total_grimoires
        )

        avg_progress = sum(
            _count_grimoires_completed(s) / total_grimoires * 100 if total_grimoires > 0 else 0
            for s in students_in_guild
        ) / count

        guilds_data.append({
            'guild': guild,
            'student_count': count,
            'average_level': round(avg_level, 1),
            'total_mana': total_mana,
            'completed_grimoires': guild_grimoires,
            'completed_spells': guild_spells,
            'progress': round(avg_progress),
        })

    students_data = []

    for student in all_students:
        membership = GuildMembership.objects.filter(
            student=student, guild__in=guilds
        ).select_related('guild').first()

        grimoires_completed = _count_grimoires_completed(student)
        spells_completed = SpellCompletion.objects.filter(student=student).count()
        progress = int(grimoires_completed / total_grimoires * 100) if total_grimoires > 0 else 0

        last_completion = SpellCompletion.objects.filter(
            student=student
        ).aggregate(last=Max('created_at'))['last']

        if last_completion:
            days_inactive = (timezone.now().date() - last_completion.date()).days
        else:
            days_inactive = 999

        has_completed_all = grimoires_completed >= total_grimoires

        students_data.append({
            'student': student,
            'guild_name': membership.guild.name if membership else '—',
            'level': student.level,
            'mana': student.mana,
            'grimoires_completed': grimoires_completed,
            'total_grimoires': total_grimoires,
            'spells_completed': spells_completed,
            'progress': progress,
            'days_inactive': days_inactive,
            'has_completed_all': has_completed_all,
        })

    alerts = _build_alerts(guilds, all_students, total_grimoires)

    students_for_json = [{
        'id': s['student'].pk,
        'name': s['student'].user.get_full_name() or s['student'].user.username,
        'initial': (s['student'].user.get_full_name() or s['student'].user.username)[0].upper(),
        'guild': s['guild_name'],
        'level': s['level'],
        'mana': s['mana'],
        'grimoires': s['grimoires_completed'],
        'total_grimoires': s['total_grimoires'],
        'spells': s['spells_completed'],
        'progress': s['progress'],
    } for s in students_data]

    context = {
        'teacher': teacher,
        'guilds': guilds,
        'metrics': metrics,
        'guilds_data': guilds_data,
        'students_data': students_data,
        'students_json': json.dumps(students_for_json, ensure_ascii=False),
        'guild_names': [g.name for g in guilds],
        'alerts': alerts[:10],
        'alerts_total': len(alerts),
    }
    return render(request, 'dashboard/teacher_dashboard.html', context)


@login_required
def guild_form(request, guild_id=None):
    if not request.user.is_teacher():
        messages.error(request, 'Acesso restrito a professores.')
        return redirect('login')

    teacher = request.user.teacher_profile

    guilds = Guild.objects.filter(
        Q(head_teacher=teacher) | Q(teachers=teacher),
        is_active=True,
    ).distinct()

    if guild_id:
        guild = get_object_or_404(
            Guild.objects.filter(Q(head_teacher=teacher) | Q(teachers=teacher)),
            pk=guild_id,
        )
    else:
        guild = None

    all_teachers = TeacherProfile.objects.select_related('user').exclude(pk=teacher.pk).order_by('user__first_name', 'user__username')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        teacher_ids = request.POST.getlist('teachers')
        is_active = request.POST.get('is_active') == 'on'

        if not name:
            messages.error(request, 'O nome da guilda é obrigatório.')
        else:
            if guild:
                guild.name = name
                guild.is_active = is_active
                guild.save()
                guild.teachers.set(teacher_ids)
                messages.success(request, f'Guilda "{guild.name}" atualizada com sucesso!')
                return redirect('dashboard:guild_detail', guild_id=guild.pk)
            else:
                guild = Guild.objects.create(
                    name=name,
                    head_teacher=teacher,
                    is_active=is_active,
                )
                if teacher_ids:
                    guild.teachers.set(teacher_ids)
                for foe in PowerfulFoe.objects.all():
                    GuildFoeProgress.objects.create(guild=guild, foe=foe)
                messages.success(request, f'Guilda "{guild.name}" criada com sucesso!')
                return redirect('dashboard:guild_detail', guild_id=guild.pk)

    selected_teacher_ids = list(guild.teachers.values_list('pk', flat=True)) if guild else []

    context = {
        'teacher': teacher,
        'guilds': guilds,
        'guild': guild,
        'all_teachers': all_teachers,
        'all_teachers_json': json.dumps([
            {'id': t.pk, 'name': t.user.get_full_name() or t.user.username}
            for t in all_teachers
        ], ensure_ascii=False),
        'selected_teacher_ids_json': json.dumps(selected_teacher_ids),
        'is_edit': guild is not None,
    }
    return render(request, 'dashboard/guild_form.html', context)


@login_required
def guild_detail(request, guild_id):
    if not request.user.is_teacher():
        messages.error(request, 'Acesso restrito a professores.')
        return redirect('login')

    teacher = request.user.teacher_profile

    guild = get_object_or_404(
        Guild.objects.filter(
            Q(head_teacher=teacher) | Q(teachers=teacher),
            is_active=True,
        ),
        pk=guild_id,
    )

    memberships = GuildMembership.objects.filter(guild=guild).select_related(
        'student__user'
    )

    students_in_guild = [m.student for m in memberships]
    total_grimoires = Grimoire.objects.count()

    student_count = len(students_in_guild)
    total_mana = sum(s.mana for s in students_in_guild)
    avg_level = round(sum(s.level for s in students_in_guild) / student_count, 1) if student_count > 0 else 0

    total_spells = SpellCompletion.objects.filter(
        student__in=students_in_guild
    ).count()

    total_grim = sum(
        _count_grimoires_completed(s) for s in students_in_guild
    )

    avg_progress = round(sum(
        _count_grimoires_completed(s) / total_grimoires * 100 if total_grimoires > 0 else 0
        for s in students_in_guild
    ) / student_count) if student_count > 0 else 0

    hero = {
        'total_mana': total_mana,
        'total_spells': total_spells,
        'total_grimoires': total_grim,
        'avg_level': avg_level,
        'avg_progress': avg_progress,
        'student_count': student_count,
        'teacher_name': teacher.user.get_full_name() or teacher.user.username,
        'school': teacher.school,
    }

    ranking = sorted(students_in_guild, key=lambda s: (-s.mana, s.created_at))[:5]
    ranking_data = []
    for i, s in enumerate(ranking):
        ranking_data.append({
            'student': s,
            'position': i + 1,
            'progress': round(_count_grimoires_completed(s) / total_grimoires * 100) if total_grimoires > 0 else 0,
            'mana': s.mana,
        })

    students_data = []
    for s in students_in_guild:
        grimoires_completed = _count_grimoires_completed(s)
        spells_completed = SpellCompletion.objects.filter(student=s).count()
        progress = round(grimoires_completed / total_grimoires * 100) if total_grimoires > 0 else 0
        students_data.append({
            'student': s,
            'level': s.level,
            'mana': s.mana,
            'grimoires_completed': grimoires_completed,
            'total_grimoires': total_grimoires,
            'spells_completed': spells_completed,
            'progress': progress,
        })

    current_foe = guild.current_foe()
    foe_data = None
    if current_foe:
        guild_total_mana = guild.total_mana()
        foe_mana_required = current_foe.foe.mana_required(student_count)
        foe_progress = min(100, int(guild_total_mana / foe_mana_required * 100)) if foe_mana_required > 0 else 0

        recent = sorted(students_in_guild, key=lambda s: (-s.mana, s.created_at))[:5]
        recent_contributions = []
        for s in recent:
            recent_contributions.append({
                'name': s.user.get_full_name() or s.user.username,
                'mana': s.mana,
            })

        contributing_count = sum(1 for s in students_in_guild if s.mana > 0)

        foe_data = {
            'name': current_foe.foe.name,
            'progress': foe_progress,
            'guild_total_mana': guild_total_mana,
            'foe_mana_required': foe_mana_required,
            'contributing_count': contributing_count,
            'remaining_count': student_count - contributing_count,
            'recent_contributions': recent_contributions,
        }

    guilds = Guild.objects.filter(
        Q(head_teacher=teacher) | Q(teachers=teacher),
        is_active=True,
    ).distinct()

    context = {
        'guild': guild,
        'teacher': teacher,
        'guilds': guilds,
        'hero': hero,
        'ranking_data': ranking_data,
        'students_data': students_data,
        'foe_data': foe_data,
    }
    return render(request, 'dashboard/guild_detail.html', context)


@login_required
def teacher_progress(request):
    if not request.user.is_teacher():
        messages.error(request, 'Acesso restrito a professores.')
        return redirect('login')

    teacher = request.user.teacher_profile

    guilds = Guild.objects.filter(
        Q(head_teacher=teacher) | Q(teachers=teacher),
        is_active=True,
    ).distinct()

    all_students = StudentProfile.objects.filter(
        guild_memberships__guild__in=guilds
    ).distinct()

    total_grimoires = Grimoire.objects.count()
    now = timezone.now()

    guild_filter = request.GET.get('guild', '').strip()
    status_filter = request.GET.get('status', '').strip()
    level_filter = request.GET.get('level', '').strip()
    search_query = request.GET.get('search', '').strip()

    students_data = []
    for student in all_students:
        membership = GuildMembership.objects.filter(
            student=student, guild__in=guilds
        ).select_related('guild').first()

        grimoires_completed = _count_grimoires_completed(student)
        spells_completed = SpellCompletion.objects.filter(student=student).count()
        progress = int(grimoires_completed / total_grimoires * 100) if total_grimoires > 0 else 0

        last_completion = SpellCompletion.objects.filter(
            student=student
        ).aggregate(last=Max('created_at'))['last']

        if last_completion:
            days_inactive = (now.date() - last_completion.date()).days
            if days_inactive == 0:
                last_activity_label = "Hoje"
            elif days_inactive == 1:
                last_activity_label = "Ontem"
            else:
                last_activity_label = f"{days_inactive} dias"
        else:
            days_inactive = 999
            last_activity_label = "Nunca"

        if days_inactive >= 10:
            status = 'inativo'
        elif days_inactive >= 5:
            status = 'risco'
        else:
            status = 'avancando'

        if days_inactive <= 2:
            tendency = 'up'
        elif days_inactive <= 7:
            tendency = 'flat'
        else:
            tendency = 'down'

        guild_name = membership.guild.name if membership else '—'

        if guild_filter and guild_name != guild_filter:
            continue
        if status_filter:
            if status_filter == 'Avançando' and status != 'avancando':
                continue
            if status_filter == 'Em risco' and status != 'risco':
                continue
            if status_filter == 'Sem atividade' and status != 'inativo':
                continue
        if level_filter:
            parts = level_filter.split('–')
            lo, hi = int(parts[0]), int(parts[1])
            if student.level < lo or student.level > hi:
                continue
        if search_query:
            full_name = student.user.get_full_name() or student.user.username
            if search_query.lower() not in full_name.lower():
                continue

        students_data.append({
            'name': student.user.get_full_name() or student.user.username,
            'initial': (student.user.get_full_name() or student.user.username)[0].upper(),
            'guild_name': guild_name,
            'level': student.level,
            'mana': student.mana,
            'grimoires_completed': grimoires_completed,
            'total_grimoires': total_grimoires,
            'spells_completed': spells_completed,
            'progress': progress,
            'status': status,
            'tendency': tendency,
            'days_inactive': days_inactive,
            'last_activity_label': last_activity_label,
        })

    avancando_count = sum(1 for s in students_data if s['status'] == 'avancando')
    risco_count = sum(1 for s in students_data if s['status'] == 'risco')
    inativo_count = sum(1 for s in students_data if s['status'] == 'inativo')

    filters_active = bool(guild_filter or status_filter or level_filter or search_query)

    guild_names = [g.name for g in guilds]

    context = {
        'teacher': teacher,
        'guilds': guilds,
        'students_data': students_data,
        'total_count': len(students_data),
        'avancando_count': avancando_count,
        'risco_count': risco_count,
        'inativo_count': inativo_count,
        'guild_names': guild_names,
        'current_guild': guild_filter,
        'current_status': status_filter,
        'current_level': level_filter,
        'current_search': search_query,
        'filters_active': filters_active,
    }
    return render(request, 'dashboard/teacher_progress.html', context)


@login_required
def teacher_alerts(request):
    if not request.user.is_teacher():
        messages.error(request, 'Acesso restrito a professores.')
        return redirect('login')

    teacher = request.user.teacher_profile

    guilds = Guild.objects.filter(
        Q(head_teacher=teacher) | Q(teachers=teacher),
        is_active=True,
    ).distinct()

    all_students = StudentProfile.objects.filter(
        guild_memberships__guild__in=guilds
    ).distinct()

    total_grimoires = Grimoire.objects.count()
    alerts = _build_alerts(guilds, all_students, total_grimoires)

    guild_names = [g.name for g in guilds]

    context = {
        'teacher': teacher,
        'guilds': guilds,
        'alerts': alerts,
        'alerts_total': len(alerts),
        'guild_names': guild_names,
    }
    return render(request, 'dashboard/teacher_alerts.html', context)


def _build_alerts(guilds, all_students, total_grimoires):
    alerts = []

    for student in all_students:
        membership = GuildMembership.objects.filter(
            student=student, guild__in=guilds
        ).select_related('guild').first()

        grimoires_completed = _count_grimoires_completed(student)
        progress = int(grimoires_completed / total_grimoires * 100) if total_grimoires > 0 else 0

        last_completion = SpellCompletion.objects.filter(
            student=student
        ).aggregate(last=Max('created_at'))['last']

        if last_completion:
            days_inactive = (timezone.now().date() - last_completion.date()).days
        else:
            days_inactive = 999

        has_completed_all = grimoires_completed >= total_grimoires

        if not has_completed_all:
            guild_name = membership.guild.name if membership else '—'
            if days_inactive >= 5:
                alerts.append({
                    'student_name': student.user.get_full_name() or student.user.username,
                    'guild_name': guild_name,
                    'message': f'Sem atividade há {days_inactive} dias',
                    'type': 'inativo',
                    'days_inactive': days_inactive,
                })
            else:
                alerts.append({
                    'student_name': student.user.get_full_name() or student.user.username,
                    'guild_name': guild_name,
                    'message': f'Progresso em {progress}% — faltam {total_grimoires - grimoires_completed} grimórios',
                    'type': 'risco',
                    'days_inactive': days_inactive,
                })

    return alerts


def _count_grimoires_completed(student: StudentProfile) -> int:
    count = 0
    for grimoire in Grimoire.objects.all():
        if grimoire.is_completed_by(student):
            count += 1
    return count


def _compute_grimoire_status(student, grimoire):
    required_total = grimoire.required_spell_count()
    if required_total == 0:
        return 'available', 0

    completed_required = grimoire.completed_required_count(student)

    if grimoire.is_completed_by(student):
        return 'completed', completed_required
    elif not grimoire.is_unlocked_for(student):
        return 'blocked', completed_required
    elif completed_required > 0:
        return 'in_progress', completed_required
    else:
        return 'available', completed_required


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
        required_total = grimoire.required_spell_count()
        total_all = grimoire.spells.count()
        total_grimoires += 1
        status, completed_count = _compute_grimoire_status(student, grimoire)

        if status == 'completed':
            completed_grimoires += 1
        elif status != 'blocked' and total_all > 0:
            completed_all = SpellCompletion.objects.filter(
                student=student,
                spell__grimoire=grimoire
            ).values('spell').distinct().count()
            pending_spells += total_all - completed_all

        earned_xp = 0
        bonus_mana = 0
        if status != 'blocked' and completed_count > 0:
            earned_xp = SpellCompletion.objects.filter(
                student=student,
                spell__grimoire=grimoire
            ).aggregate(total_xp=models.Sum('spell__mana_reward'))['total_xp'] or 0
            if grimoire.is_completed_by(student):
                bonus_mana = grimoire.mana_reward

        grimoires_data.append({
            'grimoire': grimoire,
            'total': required_total,
            'completed': completed_count,
            'status': status,
            'progress': int(completed_count / required_total * 100) if required_total > 0 else 0,
            'total_xp': grimoire.total_xp(),
            'earned_xp': earned_xp,
            'bonus_mana': bonus_mana,
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
