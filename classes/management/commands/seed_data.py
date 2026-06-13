from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from accounts.models import User, TeacherProfile, StudentProfile
from classes.models import Guild, GuildMembership, GuildFoeProgress, PowerfulFoe
from content.models import Grimoire, Spell, SpellCompletion


TEACHER_DATA = {
    "username": "professor",
    "email": "professor@teste.com",
    "password": "senha123",
    "first_name": "Camila",
    "last_name": "Ramos",
    "school": "EMEF Monteiro Lobato",
}

GUILD_NAMES = [
    "Guardiões do Código",
    "Magos da Lógica",
    "Alquimistas Digitais",
]

STUDENT_NAMES = [
    "Ana Beatriz Oliveira",
    "Bruno Costa Santos",
    "Carla Dias Lima",
    "Diego Esteves Pereira",
    "Eduarda Faria Silva",
    "Felipe Gomes Souza",
    "Gabriela Henrique Alves",
    "Heitor Iglesias Moreira",
    "Isabela Junqueira Braga",
    "João Kleber Campos",
    "Karen Lopes Teixeira",
    "Leonardo Marques Rocha",
    "Mariana Nunes Barbosa",
    "Nathan Oliveira Castro",
    "Patrícia Paula Dutra",
    "Rafael Queiroz Borges",
    "Sabrina Reis Carvalho",
    "Thiago Santos Neves",
    "Úrsula Tavares Lima",
    "Victor Uchoa Mendes",
    "Wanessa Valente Cruz",
    "Xavier Ventura Fonseca",
    "Yara Wanderley Torres",
    "Zeca Almeida Junior",
    "Alice Bernardes Couto",
    "Caio Drumond Ferreira",
    "Larissa Evangelista Souza",
    "Marcos Figueiredo Neto",
    "Nathalia Garcia Pires",
    "Otávio Heringer Duarte",
]

COMPLETION_LEVELS = [
    ("advanced", 9),
    ("medium", 6),
    ("medium", 6),
    ("medium", 6),
    ("medium", 6),
    ("low", 3),
    ("low", 3),
    ("low", 3),
    ("beginner", 2),
    ("beginner", 1),
]

INACTIVITY_DAYS = [0, 0, 1, 1, 2, 3, 4, 6, 8, 14]


def _recalculate_foe_progress(guild):
    """Recalculate foe defeated/contributed state based on current guild mana."""
    total_mana = guild.total_mana()

    for fp in GuildFoeProgress.objects.filter(
        guild=guild
    ).select_related('foe').order_by('foe__order'):
        needed = fp.foe.mana_required(guild.student_count())
        if total_mana >= needed:
            fp.defeated = True
            fp.total_mana_contributed = needed
        else:
            fp.defeated = False
            fp.total_mana_contributed = total_mana
        fp.save()


@transaction.atomic
def seed():
    """Run seed. Safe to call multiple times — recalculates foe progress on each run."""
    now = timezone.now()

    # ── Teacher ──────────────────────────────────────────────
    teacher_user = User.objects.filter(username=TEACHER_DATA["username"]).first()
    if teacher_user:
        teacher = teacher_user.teacher_profile
        print(f"Teacher found: {teacher}")
    else:
        user = User.objects.create_user(
            username=TEACHER_DATA["username"],
            email=TEACHER_DATA["email"],
            password=TEACHER_DATA["password"],
            first_name=TEACHER_DATA["first_name"],
            last_name=TEACHER_DATA["last_name"],
            role=User.Role.TEACHER,
        )
        teacher = user.teacher_profile
        teacher.school = TEACHER_DATA["school"]
        teacher.save()
        print(f"Teacher created: {teacher}")

    # ── Grimoires & Spells ───────────────────────────────────
    grimoires = list(Grimoire.objects.order_by("order"))
    all_spells_ordered = [s for g in grimoires for s in g.spells.order_by("order")]

    # ── Guilds ────────────────────────────────────────────────
    guilds = []
    for name in GUILD_NAMES:
        guild = Guild.objects.filter(name=name).first()
        if guild:
            print(f"Guild found: {guild.name}")
        else:
            guild = Guild.objects.create(name=name, head_teacher=teacher)
            for foe in PowerfulFoe.objects.order_by("order"):
                GuildFoeProgress.objects.create(guild=guild, foe=foe)
            print(f"Guild created: {guild.name}")
        guilds.append(guild)

    # ── Students (skip if already created) ────────────────────
    first_batch = User.objects.filter(username="aluno_01").exists()
    if not first_batch:
        student_idx = 0
        for guild in guilds:
            for si in range(10):
                name = STUDENT_NAMES[student_idx]
                first, *rest = name.split(" ")
                last = " ".join(rest)

                user = User.objects.create_user(
                    username=f"aluno_{student_idx + 1:02d}",
                    email=f"aluno{student_idx + 1:02d}@teste.com",
                    password="senha123",
                    first_name=first,
                    last_name=last,
                    role=User.Role.STUDENT,
                )
                student = user.student_profile
                GuildMembership.objects.create(student=student, guild=guild)

                label, num_spells = COMPLETION_LEVELS[si]
                spells_to_do = all_spells_ordered[:num_spells]
                days_ago = INACTIVITY_DAYS[si]

                for spell in spells_to_do:
                    completion = SpellCompletion.objects.create(student=student, spell=spell)
                    fake_created = now - timedelta(days=days_ago)
                    SpellCompletion.objects.filter(pk=completion.pk).update(
                        created_at=fake_created
                    )

                print(
                    f"  [{guild.name}] {user.get_full_name()} — "
                    f"{num_spells}/9 spells ({label}), "
                    f"level {student.level}, {student.mana} mana"
                )
                student_idx += 1
    else:
        print("Students already exist — skipping creation.")

    # ── Recalculate foe progress ──────────────────────────────
    for guild in guilds:
        _recalculate_foe_progress(guild)

    # ── Summary ───────────────────────────────────────────────
    print()
    print("─" * 50)
    for guild in guilds:
        fp = GuildFoeProgress.objects.filter(guild=guild).order_by('foe__order').first()
        current = GuildFoeProgress.objects.filter(guild=guild, defeated=False).order_by('foe__order').first()
        total_students = GuildMembership.objects.filter(guild=guild).count()
        total_foes = GuildFoeProgress.objects.filter(guild=guild).count()
        defeated = GuildFoeProgress.objects.filter(guild=guild, defeated=True).count()
        if current:
            progress = current.progress_percent()
            print(f"  {guild.name}: {total_students} students, {defeated}/{total_foes} foes defeated, current: {current.foe.name} ({progress:.0f}%)")
        else:
            print(f"  {guild.name}: {total_students} students, all foes defeated! 🎉")
    print("Seed complete!")


class Command(BaseCommand):
    help = "Seed test data for teacher dashboards"

    def handle(self, *args, **options):
        seed()
