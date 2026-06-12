from django.core.management.base import BaseCommand
from content.models import Badge, Grimoire, Spell, SpellCompletion, UserBadge


TOOLBOX_BASIC = {
    "kind": "categoryToolbox",
    "contents": [
        {
            "kind": "category",
            "name": "Texto",
            "colour": "#5BA58C",
            "contents": [
                {"kind": "block", "type": "text"},
                {"kind": "block", "type": "text_print"},
                {"kind": "block", "type": "text_join"},
            ]
        },
        {
            "kind": "category",
            "name": "Variáveis",
            "colour": "#A65C81",
            "custom": "VARIABLE"
        },
    ]
}

TOOLBOX_LOGIC = {
    "kind": "categoryToolbox",
    "contents": [
        {
            "kind": "category",
            "name": "Lógica",
            "colour": "#5C81A6",
            "contents": [
                {"kind": "block", "type": "controls_if"},
                {"kind": "block", "type": "logic_compare"},
                {"kind": "block", "type": "logic_operation"},
                {"kind": "block", "type": "logic_boolean"},
            ]
        },
        {
            "kind": "category",
            "name": "Texto",
            "colour": "#5BA58C",
            "contents": [
                {"kind": "block", "type": "text"},
                {"kind": "block", "type": "text_print"},
                {"kind": "block", "type": "text_join"},
            ]
        },
        {
            "kind": "category",
            "name": "Matemática",
            "colour": "#5CA65C",
            "contents": [
                {"kind": "block", "type": "math_number"},
                {"kind": "block", "type": "math_arithmetic"},
            ]
        },
        {
            "kind": "category",
            "name": "Variáveis",
            "colour": "#A65C81",
            "custom": "VARIABLE"
        },
    ]
}

TOOLBOX_LOOPS = {
    "kind": "categoryToolbox",
    "contents": [
        {
            "kind": "category",
            "name": "Laços",
            "colour": "#5CA65C",
            "contents": [
                {"kind": "block", "type": "controls_repeat_ext"},
                {"kind": "block", "type": "controls_whileUntil"},
            ]
        },
        {
            "kind": "category",
            "name": "Lógica",
            "colour": "#5C81A6",
            "contents": [
                {"kind": "block", "type": "controls_if"},
                {"kind": "block", "type": "logic_compare"},
            ]
        },
        {
            "kind": "category",
            "name": "Texto",
            "colour": "#5BA58C",
            "contents": [
                {"kind": "block", "type": "text"},
                {"kind": "block", "type": "text_print"},
                {"kind": "block", "type": "text_join"},
            ]
        },
        {
            "kind": "category",
            "name": "Matemática",
            "colour": "#5CA65C",
            "contents": [
                {"kind": "block", "type": "math_number"},
                {"kind": "block", "type": "math_arithmetic"},
            ]
        },
        {
            "kind": "category",
            "name": "Variáveis",
            "colour": "#A65C81",
            "custom": "VARIABLE"
        },
    ]
}


class Command(BaseCommand):
    help = 'Popula dados iniciais de conteúdo (badges, grimórios, feitiços) com configuração Blockly'

    def handle(self, *args, **options):
        self._clear_data()
        self._create_badges()
        self._create_grimoires()
        self.stdout.write(self.style.SUCCESS('Conteúdo inicial criado com sucesso!'))

    def _clear_data(self):
        self.stdout.write('Limpando dados existentes...')
        SpellCompletion.objects.all().delete()
        UserBadge.objects.all().delete()
        Spell.objects.all().delete()
        Grimoire.objects.all().delete()
        self.stdout.write('  Dados antigos removidos.')

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
                               'Vamos começar com comandos simples para imprimir mensagens e usar variáveis.',
                'order': 1,
                'icon': 'wand',
                'mana_reward': 50,
                'depends_on': [],
                'spells': [
                    {
                        'title': 'Primeiro Feitiço',
                        'difficulty': 'easy',
                        'is_required': True,
                        'tip': 'Procure pelo bloco "imprimir" na categoria Texto. Conecte um bloco de texto com a mensagem.',
                        'description': 'Seu primeiro feitiço! Use o bloco "imprimir" para mostrar a mensagem "Olá, Mago!" na tela.',
                        'expected_output': 'Olá, Mago!',
                        'required_block_types': ['text_print'],
                        'blockly_toolbox': {
                            "kind": "categoryToolbox",
                            "contents": [
                                {
                                    "kind": "category", "name": "Texto", "colour": "#5BA58C",
                                    "contents": [
                                        {"kind": "block", "type": "text"},
                                        {"kind": "block", "type": "text_print"},
                                    ]
                                },
                            ]
                        },
                    },
                    {
                        'title': 'Saudação ao Mago',
                        'difficulty': 'easy',
                        'is_required': True,
                        'tip': 'Crie a variável "nome" clicando em "Criar variável..." na categoria Variáveis. '
                               'Atribua o valor "Mago" a ela e use junção de texto para montar a saudação.',
                        'description': 'Crie uma variável chamada "nome", atribua o valor "Mago" a ela, '
                                      'e imprima "Bem-vindo, {nome}!" usando junção de texto.',
                        'expected_output': 'Bem-vindo, Mago!',
                        'required_block_types': ['text_print', 'variables_set'],
                        'blockly_toolbox': TOOLBOX_BASIC,
                    },
                    {
                        'title': 'Contagem Regressiva',
                        'difficulty': 'medium',
                        'is_required': True,
                        'tip': 'Crie uma variável "contador" com valor 3. Use um laço "repetir 4 vezes". '
                               'A cada repetição: imprima o contador e depois diminua ele em 1.',
                        'description': 'Use um laço de repetição para contar de 3 até 0. '
                                      'Crie uma variável "contador" que começa em 3 e diminui a cada repetição. '
                                      'Imprima o valor do contador a cada iteração.',
                        'expected_output': '3\n2\n1\n0',
                        'required_block_types': ['math_arithmetic', 'variables_set'],
                        'alternative_block_types': [['controls_repeat_ext', 'controls_whileUntil']],
                        'blockly_toolbox': TOOLBOX_LOOPS,
                    },
                ],
            },
            {
                'title': 'Condições e Decisões',
                'description': 'Aprenda a usar condicionais na programação.',
                'text_content': 'Neste grimório, você aprenderá sobre estruturas condicionais. '
                               'Elas permitem que seu programa tome decisões baseadas em condições.',
                'order': 2,
                'icon': 'code',
                'mana_reward': 80,
                'depends_on': ['Fundamentos da Magia'],
                'spells': [
                    {
                        'title': 'A Porta Mágica',
                        'difficulty': 'easy',
                        'is_required': True,
                        'tip': 'Use o bloco "se" da categoria Lógica. Compare a variável "senha" com o texto "arcano" '
                               'usando o bloco de comparação (=). Se for igual, imprima "A porta abriu!". '
                               'Senão, imprima "Acesso negado!".',
                        'description': 'Um mago precisa atravessar uma porta mágica. '
                                      'Crie uma variável "senha" com o valor "arcano". '
                                      'Use uma estrutura condicional: se "senha" for igual a "arcano", '
                                      'imprima "A porta abriu!". Senão, imprima "Acesso negado!".',
                        'expected_output': 'A porta abriu!',
                        'required_block_types': ['controls_if', 'logic_compare', 'variables_set'],
                        'blockly_toolbox': TOOLBOX_LOGIC,
                    },
                    {
                        'title': 'Temperatura Mágica',
                        'difficulty': 'medium',
                        'is_required': True,
                        'tip': 'Use o bloco "se" com "senão se". Adicione condições clicando na engrenagem. '
                               'A variável "temperatura" deve ser 35. Compare com 30 e 20.',
                        'description': 'O caldeirão mágico tem uma temperatura. '
                                      'Crie uma variável "temperatura" com o valor 35. '
                                      'Se a temperatura for maior que 30, imprima "Está quente!". '
                                      'Se for maior que 20, imprima "Está agradável!". '
                                      'Senão, imprima "Está frio!".',
                        'expected_output': 'Está quente!',
                        'required_block_types': ['controls_if', 'logic_compare', 'math_number'],
                        'blockly_toolbox': TOOLBOX_LOGIC,
                    },
                    {
                        'title': 'O Caminho Correto',
                        'difficulty': 'hard',
                        'is_required': True,
                        'tip': 'Use o bloco "e" (AND) da categoria Lógica para combinar duas condições. '
                               'Crie as variáveis "tem_chave" como verdadeiro e "porta_aberta" como falso.',
                        'description': 'Para encontrar o tesouro, o mago precisa escolher o caminho seguro. '
                                      'Crie uma variável "tem_chave" com valor "true" e "porta_aberta" com valor "false". '
                                      'Se "tem_chave" for verdadeiro E "porta_aberta" for falso, imprima "Caminho seguro!". '
                                      'Senão, imprima "Perigo!".',
                        'expected_output': 'Caminho seguro!',
                        'required_block_types': ['controls_if', 'logic_operation', 'logic_compare'],
                        'blockly_toolbox': TOOLBOX_LOGIC,
                    },
                ],
            },
            {
                'title': 'Laços e Iterações',
                'description': 'Domine os laços de repetição.',
                'text_content': 'Laços de repetição são fundamentais na programação. '
                               'Eles permitem executar um bloco de código várias vezes, '
                               'seja um número fixo de repetições ou enquanto uma condição for verdadeira.',
                'order': 3,
                'icon': 'layers',
                'mana_reward': 100,
                'depends_on': ['Condições e Decisões'],
                'spells': [
                    {
                        'title': 'Colete os Cristais',
                        'difficulty': 'easy',
                        'is_required': True,
                        'tip': 'Use o bloco "repetir" da categoria Laços. '
                               'Defina o número de repetições como 3 e dentro do laço coloque o bloco "imprimir" '
                               'com o texto "Cristal coletado!".',
                        'description': 'Cristais mágicos precisam ser coletados! '
                                      'Use um laço de repetição para imprimir "Cristal coletado!" três vezes.',
                        'expected_output': 'Cristal coletado!\nCristal coletado!\nCristal coletado!',
                        'required_block_types': ['controls_repeat_ext', 'text_print'],
                        'blockly_toolbox': TOOLBOX_LOOPS,
                    },
                    {
                        'title': 'Padrão de Estrelas',
                        'difficulty': 'medium',
                        'is_required': True,
                        'tip': 'Crie uma variável "linha" começando com texto vazio. '
                               'A cada repetição do laço, adicione uma estrela usando junção de texto. '
                               'Após o laço, imprima a variável "linha".',
                        'description': 'Use um laço para construir uma linha com 5 estrelas. '
                                      'Crie uma variável "linha" que começa vazia e a cada repetição '
                                      'adicione uma estrela (*). No final do laço, imprima a linha.',
                        'expected_output': '*****',
                        'required_block_types': ['controls_repeat_ext', 'text_join', 'variables_set'],
                        'blockly_toolbox': TOOLBOX_LOOPS,
                    },
                    {
                        'title': 'A Grande Torre',
                        'difficulty': 'hard',
                        'is_required': True,
                        'tip': 'Use um laço "repetir 5 vezes". Crie uma variável "andar" começando em 1. '
                               'A cada repetição: imprima "Andar X" e aumente o andar em 1. '
                               'Depois do laço, imprima "Topo!".',
                        'description': 'Você está escalando uma torre de 5 andares. '
                                      'Use um laço para subir cada andar. '
                                      'Crie uma variável "andar" começando em 1. '
                                      'A cada repetição, imprima "Andar X" (substituindo X pelo número) '
                                      'e aumente a variável em 1. Após o laço, imprima "Topo!".',
                        'expected_output': 'Andar 1\nAndar 2\nAndar 3\nAndar 4\nAndar 5\nTopo!',
                        'required_block_types': ['controls_repeat_ext', 'math_arithmetic', 'variables_set'],
                        'blockly_toolbox': TOOLBOX_LOOPS,
                    },
                ],
            },
        ]

        grimoire_objs = {}
        for grim_data in grimoires_data:
            spells_data = grim_data.pop('spells')
            prereq_titles = grim_data.pop('depends_on', [])

            grimoire, created = Grimoire.objects.get_or_create(
                order=grim_data['order'],
                defaults=grim_data
            )
            grimoire_objs[grim_data['title']] = grimoire
            self.stdout.write(f'  Grimório: {grimoire.title}')

            for order, spell_data in enumerate(spells_data, start=1):
                Spell.objects.get_or_create(
                    grimoire=grimoire,
                    order=order,
                    defaults=spell_data
                )
                self.stdout.write(f'    Feitiço: {spell_data["title"]} ({spell_data["difficulty"]})')

        for title, prereq_titles in [
            ('Condições e Decisões', ['Fundamentos da Magia']),
            ('Laços e Iterações', ['Condições e Decisões']),
        ]:
            grimoire = grimoire_objs.get(title)
            if grimoire:
                for prereq_title in prereq_titles:
                    prereq = grimoire_objs.get(prereq_title)
                    if prereq:
                        grimoire.depends_on.add(prereq)
                        self.stdout.write(f'  Dependência: {prereq_title} → {title}')
