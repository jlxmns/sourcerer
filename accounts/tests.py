from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.models import Avatar, AvatarLevelImage, StudentProfile, TeacherProfile

User = get_user_model()


class UserModelTest(TestCase):
    def test_create_student(self):
        user = User.objects.create_user(username='aluno1', password='test123', role='student')
        self.assertTrue(user.is_student())
        self.assertFalse(user.is_teacher())

    def test_create_teacher(self):
        user = User.objects.create_user(username='prof1', password='test123', role='teacher')
        self.assertTrue(user.is_teacher())
        self.assertFalse(user.is_student())


class StudentProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='aluno1', password='test123', role='student')
        self.profile = StudentProfile.objects.get(user=self.user)

    def test_profile_created_automatically(self):
        self.assertIsNotNone(self.profile)

    def test_initial_values(self):
        self.assertEqual(self.profile.mana, 0)
        self.assertEqual(self.profile.level, 1)

    def test_add_mana_level_up(self):
        self.profile.add_mana(50)
        self.assertEqual(self.profile.mana, 50)
        self.assertEqual(self.profile.level, 1)

        self.profile.add_mana(50)
        self.assertEqual(self.profile.mana, 100)
        self.assertEqual(self.profile.level, 2)

    def test_add_mana_no_level_up(self):
        self.profile.add_mana(99)
        self.assertEqual(self.profile.level, 1)
        self.assertEqual(self.profile.mana, 99)


class AvatarModelTest(TestCase):
    def setUp(self):
        self.avatar = Avatar.objects.create(slug='mage_blue', name='Mago Azul')

    def test_avatar_creation(self):
        self.assertEqual(str(self.avatar), 'Mago Azul')

    def test_get_image_for_level_no_images(self):
        self.assertIsNone(self.avatar.get_image_for_level(1))

    def test_get_image_for_level_with_images(self):
        img1 = AvatarLevelImage.objects.create(avatar=self.avatar, level=1, image='avatars/test1.png')
        img2 = AvatarLevelImage.objects.create(avatar=self.avatar, level=3, image='avatars/test2.png')

        self.assertEqual(self.avatar.get_image_for_level(1), img1)
        self.assertEqual(self.avatar.get_image_for_level(2), img1)
        self.assertEqual(self.avatar.get_image_for_level(3), img2)
        self.assertEqual(self.avatar.get_image_for_level(5), img2)
