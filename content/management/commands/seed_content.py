from django.core.management.base import BaseCommand
from content.models import Badge, Grimoire, Spell


class Command(BaseCommand):
    help = 'Popula dados iniciais de conteúdo (badges, grimórios, feitiços)'

    def handle(self, *args, **options):
        self._create_badges()
        self._create_grimoires()
        self.stdout.write(self.style.SUCCESS('Conteúdo inicial criado com sucesso!'))

    def _create_badges(self):
        badges_data = [
            {'name': 'Primeiro Feitiço', 'condition_type': 'spell_count', 'condition_value': '1',
             'description': 'Complete seu primeiro feitiço'},
            {'name': 'Aprendiz de Feiticeiro', 'condition_type': 'spell_count', 'condition_value': '10',
             'description': 'Complete 10 feitiços'},
            {'name': 'Mago Experiente', 'condition_type': 'spell_count', 'condition_value': '25',
             'description': 'Complete 25 feitiços'},
            {'name': 'Desafiador de Dragões', 'condition_type': 'hard_spell_complete', 'condition_value': '',
             'description': 'Complete um feitiço difícil'},
            {'name': 'Nível 2', 'condition_type': 'level_reached', 'condition_value': '2',
             'description': 'Alcance o nível 2'},
            {'name': 'Nível 3', 'condition_type': 'level_reached', 'condition_value': '3',
             'description': 'Alcance o nível 3'},
            {'name': 'Nível 4', 'condition_type': 'level_reached', 'condition_value': '4',
             'description': 'Alcance o nível 4'},
            {'name': 'Colecionador de Mana', 'condition_type': 'mana_reached', 'condition_value': '500',
             'description': 'Acumule 500 de mana'},
        ]

        for data in badges_data:
            Badge.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            self.stdout.write(f'  Badge: {data["name"]}')

    def _create_grimoires(self):
        grimoires_data = [
            {
                'title': 'Fundamentos da Magia',
                'description': 'Aprenda os conceitos básicos de programação com blocos.',
                'text_content': 'Neste grimório, você aprenderá os fundamentos da programação usando blocos de montar. '
                               'Vamos começar com comandos simples de movimento e sequência.',
                'order': 1,
                'mana_reward': 50,
                'spells': [
                    {'title': 'Primeiros Passos', 'difficulty': 'easy',
                     'description': 'Use um bloco de movimento para fazer o personagem andar para frente.'},
                    {'title': 'Sequência de Comandos', 'difficulty': 'easy',
                     'description': 'Combine dois blocos de movimento em sequência.'},
                    {'title': 'Repetindo Ações', 'difficulty': 'medium',
                     'description': 'Use um laço de repetição para executar um comando várias vezes.'},
                ]
            },
            {
                'title': 'Condições e Decisões',
                'description': 'Aprenda a usar condicionais na programação.',
                'text_content': 'Neste grimório, você aprenderá sobre estruturas condicionais. '
                               'Elas permitem que seu programa tome decisões baseadas em condições.',
                'order': 2,
                'mana_reward': 80,
                'spells': [
                    {'title': 'Caminho Seguro', 'difficulty': 'easy',
                     'description': 'Use um bloco "se" para desviar de um obstáculo.'},
                    {'title': 'Labirinto', 'difficulty': 'medium',
                     'description': 'Navegue por um labirinto usando condicionais.'},
                    {'title': 'O Guardião', 'difficulty': 'hard',
                     'description': 'Derrote o guardião usando condicionais aninhadas.'},
                ]
            },
            {
                'title': 'Laços e Iterações',
                'description': 'Domine os laços de repetição.',
                'text_content': 'Laços de repetição são fundamentais na programação. '
                               'Eles permitem executar um bloco de código várias vezes.',
                'order': 3,
                'mana_reward': 100,
                'spells': [
                    {'title': 'Coleta de Itens', 'difficulty': 'easy',
                     'description': 'Use um laço "enquanto" para coletar todos os itens.'},
                    {'title': 'Padrões Mágicos', 'difficulty': 'medium',
                     'description': 'Crie padrões usando laços aninhados.'},
                    {'title': 'A Torre', 'difficulty': 'hard',
                     'description': 'Escale a torre usando laços e condicionais.'},
                ]
            },
        ]

        grimoire_objs = {}
        for grim_data in grimoires_data:
            spells = grim_data.pop('spells')
            badge = Badge.objects.filter(
                condition_type='grimoire_complete',
                condition_value=str(grim_data.get('order', 1))
            ).first()

            grimoire, created = Grimoire.objects.get_or_create(
                order=grim_data['order'],
                defaults={**grim_data, 'badge': badge}
            )
            grimoire_objs[grim_data['title']] = grimoire

            if created:
                self.stdout.write(f'  Grimório: {grimoire.title}')

            for order, spell_data in enumerate(spells, start=1):
                _, spell_created = Spell.objects.get_or_create(
                    grimoire=grimoire,
                    order=order,
                    defaults=spell_data
                )
                if spell_created:
                    self.stdout.write(f'    Feitiço: {spell_data["title"]}')

        dependencies = [
            ('Condições e Decisões', ['Fundamentos da Magia']),
            ('Laços e Iterações', ['Condições e Decisões']),
        ]
        for title, prereqs in dependencies:
            grimoire = grimoire_objs.get(title)
            if grimoire:
                for prereq_title in prereqs:
                    prereq = grimoire_objs.get(prereq_title)
                    if prereq:
                        grimoire.depends_on.add(prereq)
                        self.stdout.write(f'  Dependência: {prereq_title} → {title}')
