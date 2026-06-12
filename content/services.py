import json
import sys
import io
from xml.etree import ElementTree

from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins, safe_globals, guarded_iter_unpack_sequence, full_write_guard
from RestrictedPython.Eval import default_guarded_getitem

from content.models import Spell, SpellCompletion, Badge, UserBadge
from accounts.models import StudentProfile


EXTRA_BUILTINS = {
    'print': print,
    'range': range,
    'True': True,
    'False': False,
    'None': None,
    'list': list,
    'dict': dict,
    'tuple': tuple,
    'set': set,
    'max': max,
    'min': min,
    'sum': sum,
    'round': round,
    'enumerate': enumerate,
    'zip': zip,
    'map': map,
    'filter': filter,
    'any': any,
    'all': all,
    'sorted': sorted,
    'reversed': reversed,
}


def _safe_import(name, *args, **kwargs):
    raise ImportError(f'Não é permitido importar módulos neste ambiente.')


def execute_blockly_code(code: str) -> dict:
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    class PrintCollector:
        def _call_print(self, *args, **kwargs):
            print(*args, **kwargs)

    restricted_globals = dict(safe_globals)
    restricted_globals['__builtins__'] = dict(safe_builtins)
    restricted_globals['__builtins__'].update(EXTRA_BUILTINS)
    restricted_globals['__builtins__']['__import__'] = _safe_import
    restricted_globals['_getitem_'] = default_guarded_getitem
    restricted_globals['_getiter_'] = lambda ob: iter(ob)
    restricted_globals['_unpack_'] = guarded_iter_unpack_sequence
    restricted_globals['_write_'] = full_write_guard
    restricted_globals['_print_'] = lambda getattr: PrintCollector()

    try:
        compiled = compile_restricted(code, '<blockly>', 'exec')
        exec(compiled, restricted_globals)
        output = sys.stdout.getvalue().strip()
        return {'success': True, 'output': output}
    except SyntaxError as e:
        return {'success': False, 'error': f'Erro de sintaxe: {e}'}
    except NameError as e:
        return {'success': False, 'error': f'Variável não definida: {e}'}
    except TypeError as e:
        return {'success': False, 'error': f'Erro de tipo: {e}'}
    except Exception as e:
        return {'success': False, 'error': f'Exceção: {type(e).__name__}: {e}'}
    finally:
        sys.stdout = old_stdout


def _parse_block_types(xml_code: str) -> set:
    try:
        root = ElementTree.fromstring(xml_code)
        types = set()
        for elem in root.iter():
            local_tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
            if local_tag == 'block':
                block_type = elem.get('type')
                if block_type:
                    types.add(block_type)
        return types
    except ElementTree.ParseError:
        return set()


def validate_spell_solution(student: StudentProfile, spell: Spell, blockly_xml: str = '',
                            generated_code: str = '') -> dict:
    result = {'valid': False, 'error': '', 'output': ''}

    if not spell.expected_output and not spell.required_block_types and not spell.validation_data:
        return {'valid': True, 'error': '', 'output': ''}

    if spell.required_block_types and blockly_xml:
        found_types = _parse_block_types(blockly_xml)
        if not found_types and blockly_xml.strip():
            result['error'] = 'XML do Blockly inválido'
            return result
        missing = [t for t in spell.required_block_types if t not in found_types]
        if missing:
            result['error'] = f'Blocos obrigatórios ausentes: {", ".join(missing)}'
            return result

    if spell.alternative_block_types and blockly_xml:
        found_types = _parse_block_types(blockly_xml)
        for group in spell.alternative_block_types:
            if not any(block_type in found_types for block_type in group):
                result['error'] = f'É necessário usar um destes blocos: {", ".join(group)}'
                return result

    if spell.validation_data and blockly_xml:
        validation_type = spell.validation_data.get('type')
        if validation_type == 'xml_blocks':
            if not _validate_xml_blocks(blockly_xml, spell.validation_data):
                result['error'] = 'Estrutura de blocos incorreta'
                return result
        elif validation_type == 'contains_blocks':
            if not _validate_contains_blocks(blockly_xml, spell.validation_data):
                result['error'] = 'Blocos necessários não encontrados'
                return result

    if spell.expected_output:
        code_to_run = generated_code or blockly_xml
        exec_result = execute_blockly_code(code_to_run)
        if not exec_result['success']:
            result['error'] = exec_result['error']
            return result

        result['output'] = exec_result['output']
        if exec_result['output'].strip() != spell.expected_output.strip():
            result['error'] = f'Esperado "{spell.expected_output}" mas obteve "{exec_result["output"]}"'
            return result

    result['valid'] = True
    return result


def _validate_xml_blocks(code: str, validation_data: dict) -> bool:
    expected_blocks = validation_data.get('expected_blocks', [])
    found_types = _parse_block_types(code)
    return all(block_type in found_types for block_type in expected_blocks)


def _validate_contains_blocks(code: str, validation_data: dict) -> bool:
    required_blocks = validation_data.get('required_blocks', [])
    for block in required_blocks:
        if block not in code:
            return False
    return True


def complete_spell(student: StudentProfile, spell: Spell, code: str = '', tip_used: bool = False) -> SpellCompletion:
    completion, created = SpellCompletion.objects.get_or_create(
        student=student,
        spell=spell,
        defaults={'code_submitted': code, 'tip_used': tip_used}
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
        Badge.ConditionType.FOE_DEFEATED: _check_foe_defeated,
    }

    check_fn = condition_map.get(badge.condition_type)
    if check_fn is None:
        return False

    return check_fn(student, badge.condition_value)


def _check_grimoire_complete(student: StudentProfile, value: str) -> bool:
    from content.models import Grimoire
    try:
        grimoire = Grimoire.objects.get(pk=int(value))
    except (Grimoire.DoesNotExist, ValueError):
        return False
    return grimoire.is_completed_by(student)


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


def _check_foe_defeated(student: StudentProfile, value: str) -> bool:
    try:
        target_order = int(value)
    except ValueError:
        return False
    from classes.models import GuildFoeProgress
    return GuildFoeProgress.objects.filter(
        guild__memberships__student=student,
        foe__order=target_order,
        defeated=True,
    ).exists()
