from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import TimeStampedModel


class User(AbstractUser):
    """
    Usuário central do SOurcerer.
    Estender AbstractUser para adicionar apenas o campo papel (role).;
    Dados extras de aluno/professor ficam nos perfis separados.
    """
    class Role(models.TextChoices):
        STUDENT = 'student', 'Aluno'
        TEACHER = 'teacher', 'Professor'
        ADMIN = 'admin', 'Administrador'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)

    def is_student(self):
        return self.role == self.Role.STUDENT

    def is_teacher(self):
        return self.role == self.Role.TEACHER

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class StudentProfile(TimeStampedModel):
    """
    Dados de gamificação e personalização do aluno.
    Separado do User para não misturar autenticação com jogo.
    """
    class AvatarChoice(models.TextChoices):
        MAGE_BLUE = 'mage_blue', 'Mago Azul'
        MAGE_RED = 'mage_red', 'Mago Vermelho'
        WITCH_GREEN = 'witch_green', 'Bruxa Verde'
        WITCH_PURPLE = 'witch_purple', 'Bruxa Roxa'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        limit_choices_to={'role': User.Role.STUDENT}
    )
    avatar = models.CharField(max_length=20, choices=AvatarChoice.choices, default=AvatarChoice.MAGE_BLUE)
    mana = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)

    def add_mana(self, amount: int):
        """Adiciona mana e recalcula o nível."""
        self.mana += amount
        self.level = self._calculate_level()
        self.save()

    def _calculate_level(self):
        """Nível baseado em faixas de mana."""
        thresholds = [0, 100, 300, 600, 1000, 1500]
        for lvl, threshold in enumerate(thresholds, start=1):
            if self.mana < threshold:
                return lvl - 1
        return len(thresholds)

    def __str__(self):
        return f"Perfil de {self.user.username} - Nível {self.level}"


class TeacherProfile(TimeStampedModel):
    """
    Dados simples do professor (Arquimago).
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_profile',
        limit_choices_to={'role': User.Role.TEACHER}
    )
    school = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Prof. {self.user.get_full_name() or self.user.username}"
