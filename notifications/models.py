from django.conf import settings
from django.db import models

from core.models import TimeStampedModel


class Notification(TimeStampedModel):
    class Type(models.TextChoices):
        BADGE_EARNED = "badge_earned", "Distintivo recebido"
        LEVEL_UP = "level_up", "Subiu de nível"
        GRIMOIRE_COMPLETE = "grimoire_complete", "Grimório completo"
        SPELL_COMPLETE_HARD = "spell_complete_hard", "Feitiço difícil completo"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    type = models.CharField(max_length=30, choices=Type.choices)
    title = models.CharField(max_length=200)
    text = models.TextField(blank=True)
    link_url = models.CharField(
        max_length=500,
        blank=True,
        help_text="URL para redirecionamento ao clicar",
    )
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"
        ordering = ("-created_at",)

    def __str__(self):
        return f"[{self.user}] {self.title}"
