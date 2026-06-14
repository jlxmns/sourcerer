# Sourcerer

Plataforma educacional gamificada para ensino de lógica de programação usando blocos visuais **Blockly**. Estudantes completam feitiços (exercícios) dentro de grimórios (capítulos), ganham mana (XP), sobem de nível, conquistam distintivos (badges) e colaboram em guildas (turmas) para derrotar inimigos poderosos.

Construída com Django, Blockly, HTMX e Alpine.js.

---

## Stack Tecnológica

| Camada | Tecnologia |
|--------|-----------|
| Backend | Python 3.12+, Django 6.x |
| Frontend | Django Templates, Blockly, HTMX, Alpine.js |
| Banco de Dados | SQLite |
| Estilização | CSS customizado (padrão BEM) |
| Assets | Pillow, Lucide Icons |

---

## Temática

| Conceito Real | Nome no App |
|---|---|
| Capítulo / Módulo | **Grimório** |
| Exercício | **Feitiço** |
| XP / Pontos | **Mana** |
| Turma | **Guilda** |
| Desafio de chefe | **Inimigo Poderoso** |
| Conquista | **Distintivo** |
| Avatar / Skin | **Avatar** |

---

## Como Executar

### Requisitos

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) (recomendado) ou pip

### Linux / macOS

```bash
# Clone e entre no diretório
cd sourcerer

# Instale as dependências
uv sync

# Execute as migrações
python manage.py migrate

# Popule o banco com dados iniciais
python manage.py seed_avatars
python manage.py seed_content
python manage.py seed_classes
python manage.py seed_data

# Inicie o servidor
python manage.py runserver
```

### Windows

```powershell
# Clone e entre no diretório
cd sourcerer

# Instale as dependências
uv sync

# Execute as migrações
python manage.py migrate

# Popule o banco com dados iniciais
python manage.py seed_avatars
python manage.py seed_content
python manage.py seed_classes
python manage.py seed_data

# Inicie o servidor
python manage.py runserver
```

Acesse **http://localhost:8000** no seu navegador.

---

## Contas de Teste

| Papel | Email | Senha |
|-------|-------|-------|
| Professor | professor@teste.com | senha123 |
| Aluno | aluno01@teste.com … aluno30@teste.com | senha123 |

---

## Modelos e Suas Finalidades

### `accounts` — Usuários e Perfis

| Modelo | Finalidade |
|--------|------------|
| `User` | Modelo de usuário customizado com campo `role` (student / teacher / admin), autenticação por email |
| `Avatar` | Modelo de avatar (ex: "Mago Azul") |
| `AvatarLevelImage` | Imagens de avatar específicas por nível |
| `StudentProfile` | Progresso do aluno: mana, nível, avatar, verificação de distintivos ao ganhar mana |
| `TeacherProfile` | Metadados do professor (escola, associações com guildas) |

### `content` — Grimórios, Feitiços, Distintivos

| Modelo | Finalidade |
|--------|------------|
| `Grimoire` | Capítulo/módulo com título, descrição, ordem, ícone, recompensa de mana, pré-requisitos de desbloqueio |
| `Spell` | Exercício de programação vinculado a um grimório: dificuldade, saída esperada, configuração do toolbox Blockly, tipos de bloco obrigatórios |
| `SpellCompletion` | Registra um feitiço concluído, concede mana, verifica conclusão de grimório e distintivos |
| `Badge` | Definição de conquista com 7 tipos de condição (grimório/feitico/quantidade/nível/mana/inimigo) |
| `UserBadge` | Vincula distintivos conquistados a um aluno com slots de exibição equipáveis (1–3) |

### `classes` — Guildas e Poderosos Inimigos

| Modelo | Finalidade |
|--------|------------|
| `Guild` | Turma com código de acesso, professor líder, status de ativação |
| `GuildMembership` | Vincula um aluno a uma guilda |
| `PowerfulFoe` | Desafio de chefe com HP, imagem, descrição, ordem e distintivo associado |
| `GuildFoeProgress` | Acompanha o progresso da guilda contra um inimigo: status de derrota, mana total contribuída |

### `notifications` — Notificações no App

| Modelo | Finalidade |
|--------|------------|
| `Notification` | Notificação interna com tipo, título, texto, link e status de leitura |

### `core` — Base

| Modelo | Finalidade |
|--------|------------|
| `TimeStampedModel` | Classe abstrata que adiciona campos `created_at` e `updated_at` |

---

## Funcionalidades

- **Autenticação por papel** — login por email, redirecionamento conforme papel (aluno / professor / admin)
- **Exercícios com Blockly** — workspace de programação visual com toolbox configurável por feitiço
- **Sistema de mana e nível** — fórmula exponencial de nível, subida automática com notificações
- **Sistema de desbloqueio de grimórios** — encadeamento de pré-requisitos entre capítulos
- **Sistema de distintivos (badges)** — 7 tipos de condição, concedidos automaticamente ao cumprir requisitos
- **Sistema de guildas (turmas)** — acesso via código de 8 caracteres, agrupamento de alunos
- **Poderosos Inimigos** — desafios de chefe para a guilda, derrotados automaticamente quando a mana da guilda excede o limite, recompensa com distintivo
- **Painel do professor** — métricas, estatísticas por guilda, tabela de alunos, alertas de inatividade, filtros
- **Painel do aluno** — cartão de perfil, distintivos equipados, progresso nos grimórios, ranking na guilda, status do inimigo
- **Notificações no app** — subida de nível, grimório completo, feitiço difícil concluído, distintivo conquistado
- **Customização de avatar** — 4 avatares com imagens específicas por nível
- **Sistema de dicas** — usar uma dica reduz a recompensa de mana para 80%
- **Validação de feitiços** — execução segura com RestrictedPython, verificação de saída esperada e tipos de bloco
- **Admin completo** — todos os modelos registrados no Django admin

---

## Executando Testes

```bash
python manage.py test accounts content classes
```

---

## Dados Iniciais (Seed)

| Comando | Descrição |
|---------|-----------|
| `seed_avatars` | Cria 4 avatares |
| `seed_content` | Cria 3 grimórios, 9 feitiços, 8 distintivos |
| `seed_classes` | Cria 5 poderosos inimigos com distintivos |
| `seed_data` | Cria 1 professor, 30 alunos, 3 guildas com progresso variado |

Execute na ordem acima após `migrate`.
