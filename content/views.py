import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from accounts.models import StudentProfile
from .models import Module, Challenge, ChallengeAttempt


def module_list(request):
    modules = Module.objects.filter(is_published=True)
    return render(request, 'content/module_list.html', {'modules': modules})


def module_detail(request, slug):
    module = get_object_or_404(Module, slug=slug, is_published=True)
    challenges = module.challenges.filter(is_published=True)
    return render(
        request,
        'content/module_detail.html',
        {
            'module': module,
            'challenges': challenges,
        }
    )


@login_required
def challenge_detail(request, module_slug, challenge_id):
    module = get_object_or_404(Module, slug=module_slug, is_published=True)
    challenge = get_object_or_404(
        Challenge,
        id=challenge_id,
        module=module,
        is_published=True,
    )

    latest_attempt = None

    if request.user.is_student():
        student_profile = StudentProfile.objects.get(user=request.user)
        latest_attempt = ChallengeAttempt.objects.filter(
            student=student_profile,
            challenge=challenge
        ).first()

    return render(
        request,
        'content/challenge_detail.html',
        {
            'module': module,
            'challenge': challenge,
            'latest_attempt': latest_attempt,
        }
    )


@login_required
@require_POST
def save_attempt(request, challenge_id):
    if not request.user.is_student():
        return JsonResponse({'success': False, 'error': 'Apenas alunos podem salvar tentativas.'}, status=403)

    challenge = get_object_or_404(Challenge, id=challenge_id, is_published=True)
    student_profile = StudentProfile.objects.get(user=request.user)

    try:
        data = json.loads(request.body)
        workspace_state = data.get('workspace_state', {})
        code_generated = data.get('code_generated', '')
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido.'}, status=400)

    attempt = ChallengeAttempt.objects.create(
        student=student_profile,
        challenge=challenge,
        workspace_state=workspace_state,
        code_generated=code_generated,
    )

    return JsonResponse({
        'success': True,
        'message': 'Tentativa salva com sucesso.',
        'attempt_id': attempt.id,
    })