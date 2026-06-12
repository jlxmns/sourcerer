from django.db import models

from core.models import TimeStampedModel


class Grimoire(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    text_content = models.TextField(help_text='Conteúdo teórico do grimório')
    order = models.PositiveIntegerField(unique=True)
    mana_reward = models.PositiveIntegerField(
        default=50, help_text='Mana extra concedida ao completar todos os feitiços'
    )
    badge = models.ForeignKey(
        'Badge',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='grimoires',
        help_text='Distintivo concedido ao completar este grimório'
    )
    depends_on = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        help_text='Grimórios que devem ser completados antes deste'
    )

    class Meta:
        verbose_name = 'Grimório'
        verbose_name_plural = 'Grimórios'
        ordering = ('order',)

    def __str__(self):
        return self.title

    def total_xp(self):
        spells_sum = self.spells.aggregate(total=models.Sum('mana_reward'))['total'] or 0
        return spells_sum + self.mana_reward

    def is_unlocked_for(self, student):
        for prereq in self.depends_on.all():
            completed = SpellCompletion.objects.filter(
                student=student,
                spell__grimoire=prereq
            ).values('spell').distinct().count()
            if completed < prereq.spells.count():
                return False
        return True

    def unlock_requirements(self, student):
        missing = []
        for prereq in self.depends_on.all():
            completed = SpellCompletion.objects.filter(
                student=student,
                spell__grimoire=prereq
            ).values('spell').distinct().count()
            if completed < prereq.spells.count():
                missing.append(prereq.title)
        return missing


class Spell(models.Model):
    class Difficulty(models.TextChoices):
        EASY = 'easy', 'Fácil'
        MEDIUM = 'medium', 'Médio'
        HARD = 'hard', 'Difícil'

    DIFFICULTY_MANA = {
        Difficulty.EASY: 5,
        Difficulty.MEDIUM: 12,
        Difficulty.HARD: 30,
    }

    title = models.CharField(max_length=200)
    description = models.TextField(help_text='Enunciado do problema')
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices, default=Difficulty.EASY)
    mana_reward = models.PositiveIntegerField(editable=False)
    grimoire = models.ForeignKey(
        Grimoire, on_delete=models.CASCADE, related_name='spells'
    )
    order = models.PositiveIntegerField()
    validation_data = models.JSONField(
        blank=True, null=True,
        help_text='Dados para validação da solução (ex: blocos esperados, saída esperada)'
    )
    badge = models.ForeignKey(
        'Badge',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='spells',
        help_text='Distintivo concedido ao completar este feitiço'
    )

    class Meta:
        verbose_name = 'Feitiço'
        verbose_name_plural = 'Feitiços'
        ordering = ('grimoire', 'order')
        unique_together = ('grimoire', 'order')

    def save(self, *args, **kwargs):
        if not self.mana_reward:
            self.mana_reward = self.DIFFICULTY_MANA.get(self.difficulty, 5)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.grimoire.title} - {self.title}"


class SpellCompletion(TimeStampedModel):
    student = models.ForeignKey(
        'accounts.StudentProfile',
        on_delete=models.CASCADE,
        related_name='spell_completions'
    )
    spell = models.ForeignKey(
        Spell, on_delete=models.CASCADE, related_name='completions'
    )
    code_submitted = models.TextField(blank=True, help_text='Código Blockly submetido')

    class Meta:
        verbose_name = 'Feitiço Completado'
        verbose_name_plural = 'Feitiços Completados'
        unique_together = ('student', 'spell')

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            from notifications.models import Notification

            self.student.add_mana(self.spell.mana_reward)

            if self.spell.difficulty == Spell.Difficulty.HARD:
                Notification.objects.create(
                    user=self.student.user,
                    type=Notification.Type.SPELL_COMPLETE_HARD,
                    title=f"Feitiço difícil completo: {self.spell.title}",
                    text="Você completou um feitiço de dificuldade difícil!",
                    link_url=self.spell.grimoire and f"/content/grimoire/{self.spell.grimoire.pk}/" or "/students/perfil/",
                )

            grimoire = self.spell.grimoire
            completed_spells = SpellCompletion.objects.filter(
                student=self.student,
                spell__grimoire=grimoire
            ).values_list('spell', flat=True).distinct().count()
            total_spells = grimoire.spells.count()
            if completed_spells >= total_spells:
                self.student.add_mana(grimoire.mana_reward)
                Notification.objects.create(
                    user=self.student.user,
                    type=Notification.Type.GRIMOIRE_COMPLETE,
                    title=f"Grimório completo: {grimoire.title}",
                    text="Você completou todos os feitiços deste grimório!",
                    link_url=f"/content/grimoire/{grimoire.pk}/",
                )
                if grimoire.badge:
                    from content.models import UserBadge
                    ub, created = UserBadge.objects.get_or_create(
                        student=self.student, badge=grimoire.badge
                    )
                    if created:
                        Notification.objects.create(
                            user=self.student.user,
                            type=Notification.Type.BADGE_EARNED,
                            title=f"Distintivo recebido: {grimoire.badge.name}",
                            text="Você ganhou um novo distintivo!",
                            link_url="/students/perfil/",
                        )

    def __str__(self):
        return f"{self.student.user.username} - {self.spell.title}"


class Badge(models.Model):
    class ConditionType(models.TextChoices):
        GRIMOIRE_COMPLETE = 'grimoire_complete', 'Completar um Grimório'
        SPELL_COMPLETE = 'spell_complete', 'Completar um Feitiço'
        SPELL_COUNT = 'spell_count', 'Completar N feitiços'
        HARD_SPELL_COMPLETE = 'hard_spell_complete', 'Completar um feitiço difícil'
        LEVEL_REACHED = 'level_reached', 'Alcançar nível N'
        MANA_REACHED = 'mana_reached', 'Acumular N de mana'

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='badges/', blank=True)
    description = models.TextField(blank=True)
    condition_type = models.CharField(
        max_length=30, choices=ConditionType.choices
    )
    condition_value = models.CharField(
        max_length=100,
        help_text='Valor específico para a condição (ex: ID do grimório, número de feitiços, nível)'
    )

    class Meta:
        verbose_name = 'Distintivo'
        verbose_name_plural = 'Distintivos'

    def __str__(self):
        return self.name


class UserBadge(TimeStampedModel):
    class DisplayOrder(models.IntegerChoices):
        SLOT_1 = 1, 'Slot 1'
        SLOT_2 = 2, 'Slot 2'
        SLOT_3 = 3, 'Slot 3'

    student = models.ForeignKey(
        'accounts.StudentProfile',
        on_delete=models.CASCADE,
        related_name='badges'
    )
    badge = models.ForeignKey(
        Badge, on_delete=models.CASCADE, related_name='user_badges'
    )
    display_order = models.PositiveSmallIntegerField(
        null=True, blank=True, choices=DisplayOrder.choices,
        help_text='Posição de exibição no perfil (1-3). Deixe vazio para não exibir.'
    )

    class Meta:
        verbose_name = 'Distintivo do Aluno'
        verbose_name_plural = 'Distintivos do Aluno'
        unique_together = ('student', 'badge')

    def __str__(self):
        return f"{self.student.user.username} - {self.badge.name}"
