from django.core.management.base import BaseCommand
from classes.models import PowerfulFoe


class Command(BaseCommand):
    help = 'Popula dados iniciais de classes (poderosos inimigos)'

    def handle(self, *args, **options):
        self._create_foes()
        self.stdout.write(self.style.SUCCESS('Dados de classes criados com sucesso!'))

    def _create_foes(self):
        foes_data = [
            {'name': 'Goblin das Sombras', 'hp': 10,
             'description': 'Um pequeno goblin que rouba mana dos iniciantes.', 'order': 1},
            {'name': 'Esqueleto Guardião', 'hp': 25,
             'description': 'Um esqueleto que guarda os segredos da torre.', 'order': 2},
            {'name': 'Golem de Pedra', 'hp': 50,
             'description': 'Uma enorme criatura de pedra que exige força coletiva.', 'order': 3},
            {'name': 'Dragão de Fogo', 'hp': 100,
             'description': 'Um temível dragão que só pode ser derrotado com união.', 'order': 4},
            {'name': 'Lich das Profundezas', 'hp': 200,
             'description': 'Um lich ancestral que drena a mana de guildas inteiras.', 'order': 5},
            {'name': 'Titã Celestial', 'hp': 500,
             'description': 'A maior ameaça já registrada. Apenas guildas lendárias o derrotaram.', 'order': 6},
        ]

        for data in foes_data:
            PowerfulFoe.objects.get_or_create(
                order=data['order'],
                defaults=data
            )
            self.stdout.write(f'  Inimigo: {data["name"]} (HP: {data["hp"]})')
