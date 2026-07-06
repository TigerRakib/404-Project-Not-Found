from django.contrib import admin
from .models import Task, AnnotationImage


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'priority', 'due_date', 'user')
    list_filter = ('status', 'priority')
    search_fields = ('title', 'tags')


@admin.register(AnnotationImage)
class AnnotationImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'image', 'uploaded_at')
    list_filter = ('uploaded_at', 'user')
    search_fields = ('user__username',)
