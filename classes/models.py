from django.db import models
from django.db.models import Sum
from django.utils.crypto import get_random_string

from core.models import TimeStampedModel


class Guild(models.Model):
    name = models.CharField(max_length=200)
    join_code = models.SlugField(
        max_length=10, unique=True,
        help_text='Código para alunos entrarem na guilda'
    )
    head_teacher = models.ForeignKey(
        'accounts.TeacherProfile',
        on_delete=models.CASCADE,
        related_name='headed_guilds'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Se falso, a guilda não aparece no painel do professor'
    )
    teachers = models.ManyToManyField(
        'accounts.TeacherProfile',
        blank=True,
        related_name='guilds',
        help_text='Professores associados a esta guilda (além do head teacher)'
    )

    class Meta:
        verbose_name = 'Guilda'
        verbose_name_plural = 'Guildas'

    def save(self, *args, **kwargs):
        if not self.join_code:
            self.join_code = get_random_string(length=8).upper()
        super().save(*args, **kwargs)

    def student_count(self):
        return self.memberships.count()

    def total_mana(self):
        return self.memberships.aggregate(
            total=Sum('student__mana')
        )['total'] or 0

    def current_foe(self):
        return self.foe_progresses.filter(defeated=False).select_related('foe').first()

    def ranking(self):
        from accounts.models import StudentProfile
        return StudentProfile.objects.filter(
            guild_memberships__guild=self
        ).order_by('-mana')

    def __str__(self):
        return self.name


class GuildMembership(TimeStampedModel):
    student = models.ForeignKey(
        'accounts.StudentProfile',
        on_delete=models.CASCADE,
        related_name='guild_memberships'
    )
    guild = models.ForeignKey(
        Guild, on_delete=models.CASCADE, related_name='memberships'
    )

    class Meta:
        verbose_name = 'Membro da Guilda'
        verbose_name_plural = 'Membros da Guilda'
        unique_together = ('student', 'guild')

    def __str__(self):
        return f"{self.student.user.username} - {self.guild.name}"


class PowerfulFoe(models.Model):
    name = models.CharField(max_length=100)
    hp = models.PositiveIntegerField(
        help_text='HP base do inimigo. Mana necessário = hp * número de alunos da guilda'
    )
    image = models.ImageField(upload_to='foes/', blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(
        unique=True, help_text='Ordem de aparição (menor = enfrentado primeiro)'
    )
    badge = models.ForeignKey(
        'content.Badge',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='powerful_foes',
        help_text='Distintivo concedido a todos os membros ao derrotar este inimigo'
    )

    class Meta:
        verbose_name = 'Poderoso Inimigo'
        verbose_name_plural = 'Poderosos Inimigos'
        ordering = ('order',)

    def mana_required(self, num_students: int) -> int:
        return self.hp * num_students

    def __str__(self):
        return self.name


class GuildFoeProgress(models.Model):
    guild = models.ForeignKey(
        Guild, on_delete=models.CASCADE, related_name='foe_progresses'
    )
    foe = models.ForeignKey(
        PowerfulFoe, on_delete=models.CASCADE, related_name='guild_progresses'
    )
    defeated = models.BooleanField(default=False)
    defeated_at = models.DateTimeField(null=True, blank=True)
    total_mana_contributed = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Progresso contra Inimigo'
        verbose_name_plural = 'Progressos contra Inimigos'
        unique_together = ('guild', 'foe')

    def mana_remaining(self) -> int:
        if self.defeated:
            return 0
        required = self.foe.mana_required(self.guild.student_count())
        return max(0, required - self.total_mana_contributed)

    def progress_percent(self) -> float:
        required = self.foe.mana_required(self.guild.student_count())
        if required == 0:
            return 100.0
        return min(100.0, (self.total_mana_contributed / required) * 100)

    def __str__(self):
        return f"{self.guild.name} vs {self.foe.name}"
