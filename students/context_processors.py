from classes.models import GuildMembership
from content.models import UserBadge
from notifications.models import Notification


def student_context(request):
    if not request.user.is_authenticated or not request.user.is_student():
        return {}

    student = request.user.student_profile

    membership = GuildMembership.objects.filter(
        student=student
    ).select_related("guild").first()

    equipped_badges = UserBadge.objects.filter(
        student=student,
        display_order__isnull=False,
    ).select_related("badge").order_by("display_order")

    unread_count = Notification.objects.filter(
        user=request.user, is_read=False
    ).count()

    return {
        "student": student,
        "membership": membership,
        "equipped_badges": equipped_badges,
        "unread_count": unread_count,
    }
