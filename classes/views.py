from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum

from .models import Guild, GuildMembership, GuildFoeProgress, PowerfulFoe
from content.models import SpellCompletion


@login_required
def join_guild(request):
    if not request.user.is_student():
        messages.error(request, 'Acesso restrito a alunos.')
        return redirect('dashboard:teacher_dashboard')

    student = request.user.student_profile

    if GuildMembership.objects.filter(student=student).exists():
        messages.warning(request, 'Você já pertence a uma guilda.')
        return redirect('dashboard:student_dashboard')

    if request.method == 'POST':
        code = request.POST.get('code', '').strip().upper()
        try:
            guild = Guild.objects.get(join_code=code)
        except Guild.DoesNotExist:
            messages.error(request, 'Código de guilda inválido.')
            return redirect('classes:join_guild')

        GuildMembership.objects.create(student=student, guild=guild)

        existing_progresses = GuildFoeProgress.objects.filter(guild=guild)
        if not existing_progresses.exists():
            for foe in PowerfulFoe.objects.all():
                GuildFoeProgress.objects.create(guild=guild, foe=foe)

        messages.success(request, f'Bem-vindo à guilda "{guild.name}"!')
        return redirect('dashboard:student_dashboard')

    return render(request, 'classes/join_guild.html')


@login_required
def guild_ranking(request, guild_id):
    guild = get_object_or_404(Guild, pk=guild_id)

    if request.user.is_student():
        membership = GuildMembership.objects.filter(
            student=request.user.student_profile,
            guild=guild
        ).first()
        if not membership:
            messages.error(request, 'Você não é membro desta guilda.')
            return redirect('dashboard:student_dashboard')

    ranking = guild.ranking()

    ranking_data = []
    for idx, student in enumerate(ranking, start=1):
        total_completions = SpellCompletion.objects.filter(
            student=student
        ).count()
        ranking_data.append({
            'position': idx,
            'student': student,
            'total_completions': total_completions,
        })

    context = {
        'guild': guild,
        'ranking_data': ranking_data,
    }
    return render(request, 'classes/guild_ranking.html', context)


@login_required
def guild_foe(request, guild_id):
    guild = get_object_or_404(Guild, pk=guild_id)

    if request.user.is_student():
        membership = GuildMembership.objects.filter(
            student=request.user.student_profile,
            guild=guild
        ).first()
        if not membership:
            messages.error(request, 'Você não é membro desta guilda.')
            return redirect('dashboard:student_dashboard')

    current_foe = guild.current_foe()

    defeated_foes = GuildFoeProgress.objects.filter(
        guild=guild, defeated=True
    ).select_related('foe')

    context = {
        'guild': guild,
        'current_foe': current_foe,
        'defeated_foes': defeated_foes,
    }
    return render(request, 'classes/guild_foe.html', context)
