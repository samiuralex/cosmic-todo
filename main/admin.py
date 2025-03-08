from django.contrib import admin
from .models import Todo

# Register your models here.

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date', 'due_date', 'completed', 'priority')
    list_filter = ('completed', 'priority', 'created_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_date'
