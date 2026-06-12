from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .models import Grimoire, Spell, SpellCompletion, UserBadge
from .services import complete_spell


@login_required
def grimoire_list(request):
    if not request.user.is_student():
        from django.contrib import messages
        messages.error(request, 'Acesso restrito a alunos.')
        from django.shortcuts import redirect
        return redirect('dashboard:teacher_dashboard')

    student = request.user.student_profile

    from classes.models import GuildMembership
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
        grimoires_data.append({
            'grimoire': grimoire,
            'total': total,
            'completed': completed,
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

    from classes.models import GuildMembership
    if not GuildMembership.objects.filter(student=student).exists():
        from django.shortcuts import redirect
        return redirect('students:no_guild')

    grimoire = get_object_or_404(Grimoire, pk=grimoire_id)

    if not grimoire.is_unlocked_for(student):
        from django.contrib import messages
        messages.error(request, 'Este grimório está bloqueado. Complete os pré-requisitos primeiro.')
        return redirect('dashboard:student_dashboard')

    spells = grimoire.spells.all()

    completed_ids = set(
        SpellCompletion.objects.filter(
            student=student,
            spell__grimoire=grimoire
        ).values_list('spell_id', flat=True)
    )

    spells_data = []
    for spell in spells:
        spells_data.append({
            'spell': spell,
            'completed': spell.pk in completed_ids,
        })

    total = len(spells)
    completed_count = len(completed_ids)

    context = {
        'grimoire': grimoire,
        'spells_data': spells_data,
        'progress': f'{completed_count}/{total}',
    }
    return render(request, 'content/grimoire_detail.html', context)


@login_required
def spell_detail(request, spell_id):
    if not request.user.is_student():
        from django.contrib import messages
        messages.error(request, 'Acesso restrito a alunos.')
        from django.shortcuts import redirect
        return redirect('dashboard:teacher_dashboard')

    student = request.user.student_profile

    from classes.models import GuildMembership
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

    context = {
        'spell': spell,
        'completion': completion,
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

    code = request.POST.get('code', '')

    from content.services import validate_spell_solution
    if not validate_spell_solution(student, spell, code):
        return JsonResponse({'error': 'Solução inválida'}, status=400)

    completion = complete_spell(student, spell, code)

    from django.contrib import messages
    messages.success(request, f'Feitiço "{spell.title}" completado! +{spell.mana_reward} mana.')

    return JsonResponse({
        'success': True,
        'mana_gained': spell.mana_reward,
        'total_mana': student.mana,
        'level': student.level,
    })
