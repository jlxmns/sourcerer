from django.contrib import admin
from .models import Grimoire, Spell, SpellCompletion, Badge, UserBadge


@admin.register(Grimoire)
class GrimoireAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'mana_reward', 'badge')
    list_filter = ('badge',)
    filter_horizontal = ('depends_on',)


@admin.register(Spell)
class SpellAdmin(admin.ModelAdmin):
    list_display = ('title', 'grimoire', 'difficulty', 'mana_reward', 'order', 'badge')
    list_filter = ('difficulty', 'grimoire', 'badge')
    ordering = ('grimoire', 'order')


@admin.register(SpellCompletion)
class SpellCompletionAdmin(admin.ModelAdmin):
    list_display = ('student', 'spell', 'created_at')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'condition_type', 'condition_value')
    list_filter = ('condition_type',)


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('student', 'badge', 'display_order', 'created_at')
    list_filter = ('badge', 'display_order')
