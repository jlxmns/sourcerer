from django.core.management.base import BaseCommand
from accounts.models import Avatar


class Command(BaseCommand):
    help = 'Popula dados iniciais de avatares'

    def handle(self, *args, **options):
        avatars_data = [
            {'slug': 'mage_blue', 'name': 'Mago Azul'},
            {'slug': 'mage_red', 'name': 'Mago Vermelho'},
            {'slug': 'witch_green', 'name': 'Bruxa Verde'},
            {'slug': 'witch_purple', 'name': 'Bruxa Roxa'},
        ]

        for data in avatars_data:
            avatar, created = Avatar.objects.get_or_create(
                slug=data['slug'],
                defaults={'name': data['name']}
            )
            if created:
                self.stdout.write(f'  Avatar: {data["name"]}')
            else:
                self.stdout.write(f'  Avatar já existe: {data["name"]}')

        self.stdout.write(self.style.SUCCESS('Avatares criados com sucesso!'))
