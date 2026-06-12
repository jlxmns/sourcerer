import json
from xml.etree import ElementTree

from content.models import Spell, SpellCompletion, Badge, UserBadge
from accounts.models import StudentProfile


def validate_spell_solution(student: StudentProfile, spell: Spell, code: str) -> bool:
    if not spell.validation_data:
        return True

    validation_type = spell.validation_data.get('type')

    if validation_type == 'xml_blocks':
        return _validate_xml_blocks(code, spell.validation_data)
    elif validation_type == 'output_match':
        return _validate_output(code, spell.validation_data)
    elif validation_type == 'contains_blocks':
        return _validate_contains_blocks(code, spell.validation_data)
    elif validation_type == 'javascript':
        return _validate_javascript(code, spell.validation_data)

    return True


def _validate_xml_blocks(code: str, validation_data: dict) -> bool:
    expected_blocks = validation_data.get('expected_blocks', [])
    try:
        root = ElementTree.fromstring(code)
        found_types = {block.get('type') for block in root.iter('block')}
        return all(block_type in found_types for block_type in expected_blocks)
    except ElementTree.ParseError:
        return False


def _validate_output(code: str, validation_data: dict) -> bool:
    expected_output = validation_data.get('expected_output', '').strip()
    return code.strip() == expected_output


def _validate_contains_blocks(code: str, validation_data: dict) -> bool:
    required_blocks = validation_data.get('required_blocks', [])
    for block in required_blocks:
        if block not in code:
            return False
    return True


def _validate_javascript(code: str, validation_data: dict) -> bool:
    expected_output = validation_data.get('expected_output', '').strip()
    return code.strip() == expected_output


def complete_spell(student: StudentProfile, spell: Spell, code: str = '') -> SpellCompletion:
    validated = validate_spell_solution(student, spell, code)
    if not validated:
        raise ValueError('Solução inválida')

    completion, created = SpellCompletion.objects.get_or_create(
        student=student,
        spell=spell,
        defaults={'code_submitted': code}
    )

    if not created:
        return completion

    if spell.badge:
        UserBadge.objects.get_or_create(student=student, badge=spell.badge)

    check_badges(student)

    return completion


def check_badges(student: StudentProfile):
    all_badges = Badge.objects.all()
    user_badge_ids = UserBadge.objects.filter(
        student=student
    ).values_list('badge_id', flat=True)

    for badge in all_badges:
        if badge.pk in user_badge_ids:
            continue

        if _check_condition(student, badge):
            UserBadge.objects.create(student=student, badge=badge)


def _check_condition(student: StudentProfile, badge: Badge) -> bool:
    from django.db.models import Count

    condition_map = {
        Badge.ConditionType.GRIMOIRE_COMPLETE: _check_grimoire_complete,
        Badge.ConditionType.SPELL_COMPLETE: _check_spell_complete,
        Badge.ConditionType.SPELL_COUNT: _check_spell_count,
        Badge.ConditionType.HARD_SPELL_COMPLETE: _check_hard_spell_complete,
        Badge.ConditionType.LEVEL_REACHED: _check_level_reached,
        Badge.ConditionType.MANA_REACHED: _check_mana_reached,
    }

    check_fn = condition_map.get(badge.condition_type)
    if check_fn is None:
        return False

    return check_fn(student, badge.condition_value)


def _check_grimoire_complete(student: StudentProfile, value: str) -> bool:
    from content.models import Grimoire, SpellCompletion
    try:
        grimoire = Grimoire.objects.get(pk=int(value))
    except (Grimoire.DoesNotExist, ValueError):
        return False
    total_spells = grimoire.spells.count()
    completed = SpellCompletion.objects.filter(
        student=student,
        spell__grimoire=grimoire
    ).values('spell').distinct().count()
    return completed >= total_spells


def _check_spell_complete(student: StudentProfile, value: str) -> bool:
    from content.models import SpellCompletion
    try:
        spell_id = int(value)
    except ValueError:
        return False
    return SpellCompletion.objects.filter(
        student=student, spell_id=spell_id
    ).exists()


def _check_spell_count(student: StudentProfile, value: str) -> bool:
    from content.models import SpellCompletion
    try:
        target = int(value)
    except ValueError:
        return False
    actual = SpellCompletion.objects.filter(student=student).values('spell').distinct().count()
    return actual >= target


def _check_hard_spell_complete(student: StudentProfile, value: str = '') -> bool:
    from content.models import SpellCompletion, Spell
    return SpellCompletion.objects.filter(
        student=student,
        spell__difficulty=Spell.Difficulty.HARD
    ).exists()


def _check_level_reached(student: StudentProfile, value: str) -> bool:
    try:
        target = int(value)
    except ValueError:
        return False
    return student.level >= target


def _check_mana_reached(student: StudentProfile, value: str) -> bool:
    try:
        target = int(value)
    except ValueError:
        return False
    return student.mana >= target
