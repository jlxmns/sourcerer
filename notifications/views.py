from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import HttpResponseForbidden, HttpResponse

from .models import Notification


@login_required
def list_notifications(request):
    Notification.objects.filter(
        user=request.user,
        created_at__lt=timezone.now() - timedelta(days=30),
        is_read=False,
    ).update(is_read=True)

    notifications = Notification.objects.filter(
        user=request.user,
        is_read=False,
    )[:50]

    html_parts = []
    for n in notifications:
        html_parts.append(
            f'<a href="{n.link_url}" class="notification-item" data-id="{n.pk}">'
            f"<strong>{n.title}</strong>"
            f"<span>{n.text}</span>"
            f"</a>"
        )

    if not html_parts:
        html_parts.append(
            '<p class="notification-empty">Nenhuma notificação</p>'
        )

    return HttpResponse("".join(html_parts))


@login_required
def mark_read(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id)
    if notification.user != request.user:
        return HttpResponseForbidden()
    notification.is_read = True
    notification.save(update_fields=["is_read"])
    return HttpResponse(status=204)
