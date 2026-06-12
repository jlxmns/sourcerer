from django.contrib.auth.decorators import login_required
from django.db import models
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .models import Grimoire, Spell, SpellCompletion, UserBadge
from .services import complete_spell
from classes.models import GuildMembership


def _sidebar_context(student):
    membership = GuildMembership.objects.filter(
        student=student
    ).select_related('guild').first()

    guild_ranking = []
    current_foe = None
    guild_student_count = 0
    if membership:
        ranking = membership.guild.ranking()
        for idx, profile in enumerate(ranking, start=1):
            guild_ranking.append({
                'position': idx,
                'student': profile,
                'is_me': profile.pk == student.pk,
            })
        current_foe = membership.guild.current_foe()
        guild_student_count = membership.guild.student_count()

    equipped_badges = UserBadge.objects.filter(
        student=student
    ).exclude(display_order__isnull=True).select_related('badge').order_by('display_order')

    avatar_image = student.avatar.get_image_for_level(student.level) if student.avatar else None

    return {
        'student': student,
        'membership': membership,
        'equipped_badges': equipped_badges,
        'avatar_image': avatar_image,
        'guild_ranking': guild_ranking,
        'current_foe': current_foe,
        'guild_student_count': guild_student_count,
    }


@login_required
def grimoire_list(request):
    if not request.user.is_student():
        from django.contrib import messages
        messages.error(request, 'Acesso restrito a alunos.')
        from django.shortcuts import redirect
        return redirect('dashboard:teacher_dashboard')

    student = request.user.student_profile

    if not GuildMembership.objects.filter(student=student).exists():
        from django.shortcuts import redirect
        return redirect('students:no_guild')

    grimoires = Grimoire.objects.all().prefetch_related('spells')

    grimoires_data = []
    for grimoire in grimoires:
        total = grimoire.spells.count()
        completed = SpellCompletion.objects.filter(
            student=student,
            spell__grimoire=grimoire
        ).values('spell').distinct().count() if total > 0 else 0

        if total == 0:
            status = 'available'
        elif completed >= total:
            status = 'completed'
        elif not grimoire.is_unlocked_for(student):
            status = 'blocked'
        elif completed > 0:
            status = 'in_progress'
        else:
            status = 'available'

        grimoires_data.append({
            'grimoire': grimoire,
            'total': total,
            'completed': completed,
            'status': status,
            'unlock_requirements': grimoire.unlock_requirements(student) if status == 'blocked' else [],
        })

    context = {
        'grimoires_data': grimoires_data,
    }
    return render(request, 'content/grimoire_list.html', context)


@login_required
def grimoire_detail(request, grimoire_id):
    if not request.user.is_student():
        from django.contrib import messages
        messages.error(request, 'Acesso restrito a alunos.')
        from django.shortcuts import redirect
        return redirect('dashboard:teacher_dashboard')

    student = request.user.student_profile

    if not GuildMembership.objects.filter(student=student).exists():
        from django.shortcuts import redirect
        return redirect('students:no_guild')

    grimoire = get_object_or_404(Grimoire, pk=grimoire_id)

    if not grimoire.is_unlocked_for(student):
        from django.contrib import messages
        messages.error(request, 'Este grimório está bloqueado. Complete os pré-requisitos primeiro.')
        return redirect('dashboard:student_dashboard')

    spells = grimoire.spells.all().order_by('order')

    completed_ids = set(
        SpellCompletion.objects.filter(
            student=student,
            spell__grimoire=grimoire
        ).values_list('spell_id', flat=True)
    )

    required_total = grimoire.required_spell_count()
    completed_required = grimoire.completed_required_count(student)
    is_completed = grimoire.is_completed_by(student)

    completed_all = len(completed_ids)
    total_all = len(spells)

    earned_xp = SpellCompletion.objects.filter(
        student=student,
        spell__grimoire=grimoire
    ).aggregate(total=models.Sum('spell__mana_reward'))['total'] or 0

    bonus_mana = grimoire.mana_reward if is_completed else 0

    earned_badge_ids = set(
        UserBadge.objects.filter(
            student=student,
            badge__spells__grimoire=grimoire
        ).values_list('badge_id', flat=True)
    )

    spell_badge_ids = set(
        grimoire.spells.exclude(badge__isnull=True).values_list('badge_id', flat=True)
    )
    unearned_badge_ids = spell_badge_ids - earned_badge_ids
    available_badge_count = len(unearned_badge_ids)

    spells_data = []
    for spell in spells:
        spell_completed = spell.pk in completed_ids
        if spell_completed:
            status = 'completed'
        elif not grimoire.is_unlocked_for(student):
            status = 'blocked'
        elif completed_all > 0:
            status = 'in_progress'
        else:
            status = 'available'

        spells_data.append({
            'spell': spell,
            'completed': spell_completed,
            'status': status,
            'has_badge': spell.badge is not None,
            'badge_earned': spell.badge_id in earned_badge_ids if spell.badge else False,
        })

    context = {
        'grimoire': grimoire,
        'spells_data': spells_data,
        'is_completed': is_completed,
        'required_total': required_total,
        'completed_required': completed_required,
        'total_all': total_all,
        'completed_all': completed_all,
        'progress_pct': int(completed_required / required_total * 100) if required_total > 0 else 0,
        'earned_xp': earned_xp,
        'bonus_mana': bonus_mana,
        'total_xp': grimoire.total_xp(),
        'available_badge_count': available_badge_count,
        'has_optional_spells': any(not s.is_required for s in spells),
    }
    context.update(_sidebar_context(student))
    return render(request, 'content/grimoire_detail.html', context)


@login_required
def spell_detail(request, spell_id):
    if not request.user.is_student():
        from django.contrib import messages
        messages.error(request, 'Acesso restrito a alunos.')
        from django.shortcuts import redirect
        return redirect('dashboard:teacher_dashboard')

    student = request.user.student_profile

    if not GuildMembership.objects.filter(student=student).exists():
        from django.shortcuts import redirect
        return redirect('students:no_guild')

    spell = get_object_or_404(Spell, pk=spell_id)

    if not spell.grimoire.is_unlocked_for(student):
        from django.contrib import messages
        messages.error(request, 'Este feitiço está bloqueado. Complete os pré-requisitos do grimório primeiro.')
        return redirect('dashboard:student_dashboard')

    completion = SpellCompletion.objects.filter(
        student=student, spell=spell
    ).first()

    spells = spell.grimoire.spells.all().order_by('order')
    spell_index = None
    total_spells = len(spells)
    for idx, s in enumerate(spells, start=1):
        if s.pk == spell.pk:
            spell_index = idx
            break

    context = {
        'spell': spell,
        'completion': completion,
        'spell_index': spell_index,
        'total_spells': total_spells,
        'blockly_config': spell.blockly_toolbox,
    }
    return render(request, 'content/spell_detail.html', context)


@login_required
def spell_submit(request, spell_id):
    if not request.user.is_student():
        return JsonResponse({'error': 'Acesso restrito'}, status=403)

    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)

    student = request.user.student_profile
    spell = get_object_or_404(Spell, pk=spell_id)

    if not spell.grimoire.is_unlocked_for(student):
        return JsonResponse({'error': 'Este grimório está bloqueado'}, status=403)

    if SpellCompletion.objects.filter(student=student, spell=spell).exists():
        return JsonResponse({'error': 'Feitiço já completado'}, status=400)

    import json
    try:
        data = json.loads(request.body) if request.body else request.POST.dict()
    except json.JSONDecodeError:
        data = request.POST.dict()

    blockly_xml = data.get('blockly_xml', '')
    generated_code = data.get('generated_code', '')
    tip_used = data.get('tip_used', 'false').lower() == 'true'

    from content.services import validate_spell_solution, complete_spell

    result = validate_spell_solution(student, spell, blockly_xml=blockly_xml, generated_code=generated_code)

    if not result['valid']:
        return JsonResponse({
            'success': False,
            'error': result.get('error', 'Solução inválida'),
            'output': result.get('output', ''),
        }, status=400)

    completion = complete_spell(student, spell, generated_code, tip_used)

    mana_gained = spell.mana_reward
    if tip_used:
        mana_gained = int(mana_gained * 0.8)

    return JsonResponse({
        'success': True,
        'mana_gained': mana_gained,
        'total_mana': student.mana,
        'level': student.level,
        'output': result.get('output', ''),
    })
