from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import TimeStampedModel


class User(AbstractUser):
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


class Avatar(models.Model):
    slug = models.SlugField(max_length=30, unique=True)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Avatar'
        verbose_name_plural = 'Avatares'

    def get_image_for_level(self, level: int):
        return self.images.filter(level__lte=level).order_by('-level').first()

    def __str__(self):
        return self.name


class AvatarLevelImage(models.Model):
    avatar = models.ForeignKey(
        Avatar, on_delete=models.CASCADE, related_name='images'
    )
    level = models.PositiveIntegerField()
    image = models.ImageField(upload_to='avatars/')

    class Meta:
        verbose_name = 'Imagem de Avatar por Nível'
        verbose_name_plural = 'Imagens de Avatar por Nível'
        unique_together = ('avatar', 'level')
        ordering = ('avatar', 'level')

    def __str__(self):
        return f"{self.avatar.name} - Nível {self.level}"


class StudentProfile(TimeStampedModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        limit_choices_to={'role': User.Role.STUDENT}
    )
    avatar = models.ForeignKey(
        Avatar,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='student_profiles'
    )
    mana = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)

    def add_mana(self, amount: int):
        old_level = self.level
        self.mana += amount
        self.level = self._calculate_level()
        if self.level > old_level:
            self.check_level_badges()
            from notifications.models import Notification
            Notification.objects.create(
                user=self.user,
                type=Notification.Type.LEVEL_UP,
                title=f"Subiu para o nível {self.level}!",
                text="Parabéns! Você alcançou um novo nível.",
                link_url="/students/perfil/",
            )
        self.save()

    def _calculate_level(self):
        thresholds = [0, 100, 300, 600, 1000, 1500]
        for lvl, threshold in enumerate(thresholds, start=1):
            if self.mana < threshold:
                return lvl - 1
        return len(thresholds)

    def check_level_badges(self):
        from content.models import Badge, UserBadge
        level_badges = Badge.objects.filter(
            condition_type='level_reached',
            condition_value=str(self.level)
        )
        for badge in level_badges:
            UserBadge.objects.get_or_create(student=self, badge=badge)

    def __str__(self):
        return f"Perfil de {self.user.username} - Nível {self.level}"


class TeacherProfile(TimeStampedModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_profile',
        limit_choices_to={'role': User.Role.TEACHER}
    )
    school = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Prof. {self.user.get_full_name() or self.user.username}"
