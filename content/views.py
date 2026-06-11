from django.shortcuts import get_object_or_404, render
from .models import Module, Challenge


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


def challenge_detail(request, module_slug, challenge_id):
    module = get_object_or_404(Module, slug=module_slug, is_published=True)
    challenge = get_object_or_404(
        Challenge,
        id=challenge_id,
        module=module,
        is_published=True,
    )
    return render(
        request,
        'content/challenge_detail.html',
        {
            'module': module,
            'challenge': challenge,
        }
    )