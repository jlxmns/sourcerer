from django.contrib import admin
from .models import Grimoire, Spell, SpellCompletion, Badge, UserBadge


@admin.register(Grimoire)
class GrimoireAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'icon', 'mana_reward', 'badge')
    list_filter = ('badge',)
    filter_horizontal = ('depends_on',)


@admin.register(Spell)
class SpellAdmin(admin.ModelAdmin):
    list_display = ('title', 'grimoire', 'difficulty', 'mana_reward', 'is_required', 'order', 'badge')
    list_filter = ('difficulty', 'grimoire', 'badge', 'is_required')
    ordering = ('grimoire', 'order')
    fieldsets = (
        (None, {'fields': ('title', 'description', 'difficulty', 'grimoire', 'order', 'is_required')}),
        ('Recompensa', {'fields': ('mana_reward', 'badge')}),
        ('Blockly', {'fields': ('tip', 'blockly_toolbox', 'expected_output', 'required_block_types', 'alternative_block_types', 'validation_data')}),
    )


@admin.register(SpellCompletion)
class SpellCompletionAdmin(admin.ModelAdmin):
    list_display = ('student', 'spell', 'tip_used', 'created_at')
    list_filter = ('created_at', 'tip_used')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'condition_type', 'condition_value')
    list_filter = ('condition_type',)


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('student', 'badge', 'display_order', 'created_at')
    list_filter = ('badge', 'display_order')
