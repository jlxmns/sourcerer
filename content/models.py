from django.db import models
from core.models import TimeStampedModel


class Module(TimeStampedModel):
    class Pillar(models.TextChoices):
        DECOMPOSITION = 'decomposition', 'Decomposição'
        PATTERNS = 'patterns', 'Reconhecimento de Padrões'
        ABSTRACTION = 'abstraction', 'Abstração'
        ALGORITHMS = 'algorithms', 'Algoritmos'

    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    pillar = models.CharField(max_length=20, choices=Pillar.choices)
    order = models.PositiveIntegerField(default=1)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class Challenge(TimeStampedModel):
    class Difficulty(models.TextChoices):
        EASY = 'easy', 'Fácil'
        MEDIUM = 'medium', 'Médio'
        HARD = 'hard', 'Difícil'

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='challenges',
    )
    title = models.CharField(max_length=150)
    description = models.TextField()
    story_text = models.TextField(blank=True)
    learning_goal = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices, default=Difficulty.EASY)
    order = models.PositiveIntegerField(default=1)
    mana_reward = models.PositiveIntegerField(default=10)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'title']
        unique_together = ('module', 'order')

    def __str__(self):
        return f'{self.module.title} - {self.title}'
