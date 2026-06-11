from django.contrib import admin
from .models import Module, Challenge


class ChallengeInline(admin.TabularInline):
    model = Challenge
    extra = 1


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'pillar', 'order', 'is_published')
    list_filter = ('pillar', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ChallengeInline]


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'difficulty', 'order', 'mana_reward', 'is_published')
    list_filter = ('difficulty', 'is_published', 'module')
    search_fields = ('title', 'description', 'learning_goal')