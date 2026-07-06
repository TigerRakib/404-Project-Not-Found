from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'status', 'priority', 'due_date', 'user')
	list_filter = ('status', 'priority')
	search_fields = ('title', 'tags')
