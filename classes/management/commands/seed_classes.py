from django.core.management.base import BaseCommand
from content.models import Badge
from classes.models import PowerfulFoe


class Command(BaseCommand):
    help = 'Popula dados iniciais de classes (poderosos inimigos)'

    def handle(self, *args, **options):
        self._create_foes_and_badges()
        self.stdout.write(self.style.SUCCESS('Dados de classes criados com sucesso!'))

    def _create_foes_and_badges(self):
        foes_data = [
            {
                'name': 'Slime das Sombras',
                'hp': 10,
                'description': 'Um pequeno slime que drena a mana de feiticeiros iniciantes.',
                'order': 1,
            },
            {
                'name': 'Lobo da Neblina',
                'hp': 20,
                'description': 'Um lobo espectral que caça em bando nas florestas encantadas.',
                'order': 2,
            },
            {
                'name': 'Gárgula Vigilante',
                'hp': 30,
                'description': 'Uma gárgula desperta por magia antiga, guardiã de torres arcanas.',
                'order': 3,
            },
            {
                'name': 'Basilisco Pétreo',
                'hp': 40,
                'description': 'Criatura com olhar paralisante que transforma seus inimigos em pedra.',
                'order': 4,
            },
            {
                'name': 'Fênix Rubra',
                'hp': 100,
                'description': 'Ave lendária que renasce das próprias cinzas. Exige o poder máximo da guilda.',
                'order': 5,
            },
        ]

        for data in foes_data:
            badge, _ = Badge.objects.get_or_create(
                name=f'Derrotou {data["name"]}',
                defaults={
                    'description': f'Derrote o {data["name"]} junto com sua guilda.',
                    'condition_type': Badge.ConditionType.FOE_DEFEATED,
                    'condition_value': str(data['order']),
                },
            )
            self.stdout.write(f'  Distintivo: {badge.name}')

            foe, created = PowerfulFoe.objects.get_or_create(
                order=data['order'],
                defaults={
                    'name': data['name'],
                    'hp': data['hp'],
                    'description': data['description'],
                    'badge': badge,
                },
            )
            if not created:
                foe.name = data['name']
                foe.hp = data['hp']
                foe.description = data['description']
                foe.badge = badge
                foe.save()

            self.stdout.write(f'  Inimigo: {foe.name} (HP: {foe.hp})')
