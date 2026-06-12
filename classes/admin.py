from django.contrib import admin
from .models import Guild, GuildMembership, PowerfulFoe, GuildFoeProgress


@admin.register(Guild)
class GuildAdmin(admin.ModelAdmin):
    list_display = ('name', 'join_code', 'head_teacher')
    search_fields = ('name', 'join_code')


@admin.register(GuildMembership)
class GuildMembershipAdmin(admin.ModelAdmin):
    list_display = ('student', 'guild', 'created_at')
    list_filter = ('guild',)


@admin.register(PowerfulFoe)
class PowerfulFoeAdmin(admin.ModelAdmin):
    list_display = ('name', 'hp', 'order')
    ordering = ('order',)


@admin.register(GuildFoeProgress)
class GuildFoeProgressAdmin(admin.ModelAdmin):
    list_display = ('guild', 'foe', 'defeated', 'total_mana_contributed')
    list_filter = ('defeated', 'guild')
