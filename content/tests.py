from django.test import TestCase
from django.contrib.auth import get_user_model

from content.models import Grimoire, Spell, SpellCompletion, Badge, UserBadge
from accounts.models import StudentProfile

User = get_user_model()


class GrimoireModelTest(TestCase):
    def setUp(self):
        self.grimoire1 = Grimoire.objects.create(
            title='Fundamentos', description='Básico',
            text_content='Conteúdo teórico', order=1, mana_reward=50
        )
        self.grimoire2 = Grimoire.objects.create(
            title='Avançado', description='Intermediário',
            text_content='Conteúdo avançado', order=2, mana_reward=80
        )
        self.grimoire3 = Grimoire.objects.create(
            title='Mestre', description='Avançado',
            text_content='Conteúdo de mestre', order=3, mana_reward=100
        )
        Spell.objects.create(
            title='Spell 1', description='Desc',
            difficulty='easy', grimoire=self.grimoire1, order=1
        )
        Spell.objects.create(
            title='Spell 2', description='Desc',
            difficulty='medium', grimoire=self.grimoire2, order=1
        )

    def test_grimoire_creation(self):
        self.assertEqual(str(self.grimoire1), 'Fundamentos')
        self.assertEqual(self.grimoire1.mana_reward, 50)

    def test_depends_on_relationship(self):
        self.grimoire2.depends_on.add(self.grimoire1)
        self.assertIn(self.grimoire1, self.grimoire2.depends_on.all())

    def test_total_xp(self):
        expected = 5 + 50
        self.assertEqual(self.grimoire1.total_xp(), expected)

    def test_total_xp_with_dependencies(self):
        expected = 12 + 80
        self.assertEqual(self.grimoire2.total_xp(), expected)

    def test_is_unlocked_for_no_prereqs(self):
        user = User.objects.create_user(username='aluno', password='test123', role='student')
        student = StudentProfile.objects.get(user=user)
        self.assertTrue(self.grimoire1.is_unlocked_for(student))

    def test_is_unlocked_for_prereqs_met(self):
        user = User.objects.create_user(username='aluno', password='test123', role='student')
        student = StudentProfile.objects.get(user=user)
        self.grimoire2.depends_on.add(self.grimoire1)
        SpellCompletion.objects.create(student=student, spell=self.grimoire1.spells.first())
        self.assertTrue(self.grimoire2.is_unlocked_for(student))

    def test_is_unlocked_for_prereqs_not_met(self):
        user = User.objects.create_user(username='aluno', password='test123', role='student')
        student = StudentProfile.objects.get(user=user)
        self.grimoire2.depends_on.add(self.grimoire1)
        self.assertFalse(self.grimoire2.is_unlocked_for(student))

    def test_unlock_requirements_empty_when_met(self):
        user = User.objects.create_user(username='aluno', password='test123', role='student')
        student = StudentProfile.objects.get(user=user)
        self.grimoire2.depends_on.add(self.grimoire1)
        SpellCompletion.objects.create(student=student, spell=self.grimoire1.spells.first())
        self.assertEqual(self.grimoire2.unlock_requirements(student), [])

    def test_unlock_requirements_lists_missing(self):
        user = User.objects.create_user(username='aluno', password='test123', role='student')
        student = StudentProfile.objects.get(user=user)
        self.grimoire2.depends_on.add(self.grimoire1)
        missing = self.grimoire2.unlock_requirements(student)
        self.assertIn('Fundamentos', missing)


class SpellModelTest(TestCase):
    def setUp(self):
        self.grimoire = Grimoire.objects.create(
            title='Fundamentos', text_content='Texto', order=1
        )

    def test_spell_difficulty_mana(self):
        easy = Spell.objects.create(
            title='Fácil', description='Desc',
            difficulty='easy', grimoire=self.grimoire, order=1
        )
        self.assertEqual(easy.mana_reward, 5)

        medium = Spell.objects.create(
            title='Médio', description='Desc',
            difficulty='medium', grimoire=self.grimoire, order=2
        )
        self.assertEqual(medium.mana_reward, 12)

        hard = Spell.objects.create(
            title='Difícil', description='Desc',
            difficulty='hard', grimoire=self.grimoire, order=3
        )
        self.assertEqual(hard.mana_reward, 30)


class SpellCompletionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='aluno1', password='test123', role='student')
        self.student = StudentProfile.objects.get(user=self.user)
        self.grimoire = Grimoire.objects.create(
            title='Fundamentos', text_content='Texto', order=1, mana_reward=50
        )
        self.spell = Spell.objects.create(
            title='Primeiro', description='Desc',
            difficulty='easy', grimoire=self.grimoire, order=1
        )
        self.spell2 = Spell.objects.create(
            title='Segundo', description='Desc',
            difficulty='easy', grimoire=self.grimoire, order=2
        )

    def test_completion_adds_mana(self):
        initial_mana = self.student.mana
        SpellCompletion.objects.create(student=self.student, spell=self.spell)
        self.student.refresh_from_db()
        self.assertEqual(self.student.mana, initial_mana + 5)

    def test_duplicate_completion(self):
        SpellCompletion.objects.create(student=self.student, spell=self.spell)
        with self.assertRaises(Exception):
            SpellCompletion.objects.create(student=self.student, spell=self.spell)

    def test_grimoire_completion_extra_mana(self):
        initial = self.student.mana

        SpellCompletion.objects.create(student=self.student, spell=self.spell)
        self.student.refresh_from_db()
        mana_after_first = self.student.mana
        self.assertEqual(mana_after_first, initial + 5)

        SpellCompletion.objects.create(student=self.student, spell=self.spell2)
        self.student.refresh_from_db()
        mana_after_second = self.student.mana
        self.assertEqual(mana_after_second, mana_after_first + 5 + 50)


class BadgeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='aluno1', password='test123', role='student')
        self.student = StudentProfile.objects.get(user=self.user)
        self.badge = Badge.objects.create(
            name='Primeiro Feitiço', condition_type='spell_count',
            condition_value='1'
        )

    def test_badge_unlock(self):
        UserBadge.objects.create(student=self.student, badge=self.badge)
        self.assertEqual(self.student.badges.count(), 1)

    def test_badge_unique_per_student(self):
        UserBadge.objects.create(student=self.student, badge=self.badge)
        with self.assertRaises(Exception):
            UserBadge.objects.create(student=self.student, badge=self.badge)

    def test_display_order(self):
        ub = UserBadge.objects.create(
            student=self.student, badge=self.badge, display_order=1
        )
        self.assertEqual(ub.display_order, 1)
