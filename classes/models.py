from django.db import models
from django.utils.crypto import get_random_string
from accounts.models import User, StudentProfile, TeacherProfile
from core.models import TimeStampedModel

class SchoolClass(TimeStampedModel):
    """
    Turma criada pelo professor.
    """
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='guilds')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    invite_code = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return f"{self.name} ({self.teacher.user.username})"

    @classmethod
    def generate_invite_code(cls):
        """Gera um código único de 8 caracteres."""
        while True:
            code = get_random_string(length=8, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            if not cls.objects.filter(invite_code=code).exists():
                return code

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = self.generate_invite_code()
        super().save(*args, **kwargs)


class Enrollment(TimeStampedModel):
    """Matrícula de aluno em uma turma."""
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    guild = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student.user.username} in {self.guild.name}"
