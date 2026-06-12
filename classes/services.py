from django.utils import timezone

from classes.models import GuildFoeProgress
from content.models import UserBadge


def defeat_foe(progress: GuildFoeProgress) -> list[UserBadge]:
    if progress.defeated:
        return []

    created_badges = []

    progress.defeated = True
    progress.defeated_at = timezone.now()
    progress.save()

    badge = progress.foe.badge
    if badge:
        memberships = progress.guild.memberships.select_related('student').all()
        for membership in memberships:
            _, created = UserBadge.objects.get_or_create(
                student=membership.student,
                badge=badge,
            )
            if created:
                created_badges.append(_)

    return created_badges
