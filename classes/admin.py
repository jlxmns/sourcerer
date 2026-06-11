from django.contrib import admin
from .models import SchoolClass, Enrollment


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'invite_code', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'invite_code', 'teacher__user__username')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'guild', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
