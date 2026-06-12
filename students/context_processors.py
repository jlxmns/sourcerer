from classes.models import GuildMembership
from classes.services import defeat_foe
from content.models import UserBadge
from notifications.models import Notification


def student_context(request):
    if not request.user.is_authenticated or not request.user.is_student():
        return {}

    student = request.user.student_profile

    membership = GuildMembership.objects.filter(
        student=student
    ).select_related("guild").first()

    guild_ranking = []
    current_foe = None
    guild_student_count = 0
    guild_total_mana = 0
    foe_mana_required = 0
    foe_progress_percent = 0

    if membership:
        guild = membership.guild
        ranking = guild.ranking()
        for idx, profile in enumerate(ranking, start=1):
            guild_ranking.append({
                'position': idx,
                'student': profile,
                'is_me': profile.pk == student.pk,
            })
        current_foe = guild.current_foe()
        guild_student_count = guild.student_count()
        guild_total_mana = guild.total_mana()

        while current_foe and guild_total_mana >= current_foe.foe.mana_required(guild_student_count):
            defeat_foe(current_foe)
            current_foe = guild.current_foe()

        if current_foe:
            foe_mana_required = current_foe.foe.mana_required(guild_student_count)
            if foe_mana_required > 0:
                foe_progress_percent = min(100, int(guild_total_mana / foe_mana_required * 100))

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
        "guild_ranking": guild_ranking,
        "current_foe": current_foe,
        "guild_student_count": guild_student_count,
        "guild_total_mana": guild_total_mana,
        "foe_mana_required": foe_mana_required,
        "foe_progress_percent": foe_progress_percent,
    }
