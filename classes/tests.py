from django.test import TestCase
from django.contrib.auth import get_user_model

from classes.models import Guild, GuildMembership, PowerfulFoe, GuildFoeProgress
from accounts.models import StudentProfile, TeacherProfile

User = get_user_model()


class GuildModelTest(TestCase):
    def setUp(self):
        teacher_user = User.objects.create_user(
            username='prof', password='test123', role='teacher'
        )
        self.teacher = TeacherProfile.objects.get(user=teacher_user)
        self.guild = Guild.objects.create(
            name='Guilda Teste', head_teacher=self.teacher
        )

    def test_guild_creation(self):
        self.assertEqual(self.guild.name, 'Guilda Teste')
        self.assertEqual(self.guild.head_teacher, self.teacher)

    def test_auto_join_code(self):
        self.assertIsNotNone(self.guild.join_code)
        self.assertEqual(len(self.guild.join_code), 8)

    def test_student_count_zero(self):
        self.assertEqual(self.guild.student_count(), 0)


class GuildMembershipTest(TestCase):
    def setUp(self):
        teacher_user = User.objects.create_user(
            username='prof', password='test123', role='teacher'
        )
        student_user = User.objects.create_user(
            username='aluno', password='test123', role='student'
        )
        self.teacher = TeacherProfile.objects.get(user=teacher_user)
        self.student = StudentProfile.objects.get(user=student_user)
        self.guild = Guild.objects.create(
            name='Guilda Teste', head_teacher=self.teacher
        )

    def test_membership_creation(self):
        GuildMembership.objects.create(student=self.student, guild=self.guild)
        self.assertEqual(self.guild.student_count(), 1)

    def test_unique_membership(self):
        GuildMembership.objects.create(student=self.student, guild=self.guild)
        with self.assertRaises(Exception):
            GuildMembership.objects.create(student=self.student, guild=self.guild)

    def test_ranking(self):
        GuildMembership.objects.create(student=self.student, guild=self.guild)
        ranking = self.guild.ranking()
        self.assertIn(self.student, ranking)


class PowerfulFoeTest(TestCase):
    def setUp(self):
        self.foe = PowerfulFoe.objects.create(
            name='Goblin', hp=10, order=1
        )

    def test_mana_required(self):
        self.assertEqual(self.foe.mana_required(5), 50)
        self.assertEqual(self.foe.mana_required(10), 100)

    def test_ordering(self):
        foe2 = PowerfulFoe.objects.create(name='Dragão', hp=100, order=2)
        foes = PowerfulFoe.objects.all()
        self.assertEqual(list(foes), [self.foe, foe2])


class GuildFoeProgressTest(TestCase):
    def setUp(self):
        teacher_user = User.objects.create_user(
            username='prof', password='test123', role='teacher'
        )
        self.teacher = TeacherProfile.objects.get(user=teacher_user)
        self.guild = Guild.objects.create(
            name='Guilda Teste', head_teacher=self.teacher
        )
        self.foe = PowerfulFoe.objects.create(
            name='Goblin', hp=10, order=1
        )
        self.progress = GuildFoeProgress.objects.create(
            guild=self.guild, foe=self.foe
        )

    def test_initial_progress(self):
        self.assertFalse(self.progress.defeated)
        self.assertEqual(self.progress.total_mana_contributed, 0)

    def test_mana_remaining(self):
        from accounts.models import StudentProfile
        student_user = User.objects.create_user(
            username='aluno', password='test123', role='student'
        )
        student = StudentProfile.objects.get(user=student_user)
        GuildMembership.objects.create(student=student, guild=self.guild)

        required = self.foe.mana_required(1)
        self.assertEqual(required, 10)
        self.assertEqual(self.progress.mana_remaining(), required)

        self.progress.total_mana_contributed = 10
        self.assertEqual(self.progress.mana_remaining(), 0)

    def test_progress_percent(self):
        from accounts.models import StudentProfile
        student_user = User.objects.create_user(
            username='aluno', password='test123', role='student'
        )
        student = StudentProfile.objects.get(user=student_user)
        GuildMembership.objects.create(student=student, guild=self.guild)

        self.assertEqual(self.progress.progress_percent(), 0.0)

        self.progress.total_mana_contributed = 5
        self.assertEqual(self.progress.progress_percent(), 50.0)

        self.progress.total_mana_contributed = 10
        self.progress.defeated = True
        self.assertEqual(self.progress.mana_remaining(), 0)
