from django.contrib import admin
from django.db.models import Count

from . import models

# Register your models here.

admin.site.register(models.Category)


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'user', 'category', 'tasks_count', 'created_at']
    list_per_page = 20
    list_editable = ['status']
    list_select_related = ['category', 'user']

    def tasks_count(self, obj):
        return obj.tasks_count

    def get_queryset(self, request):
        query = super().get_queryset(request)
        query = query.annotate(tasks_count=Count('task'))
        return query


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'is_done', 'project']
    list_per_page = 20
    list_editable = ['is_done']

