from django.contrib import admin
from .models import Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
	list_display = ('id', 'question', 'answer', 'status', 'datetime', 'username_id')
	list_filter = ('id', 'question', 'answer', 'status', 'datetime', 'username_id')
	ordering = ('id', 'question', 'answer', 'status', 'datetime', 'username_id')