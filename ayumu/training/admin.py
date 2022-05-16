from django.contrib import admin
from .models import Translation, Result


@admin.register(Translation)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('id', 'eng', 'rus')
	ordering = ('id', 'eng', 'rus')

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
	list_display = ('id', 'question', 'answer', 'status', 'datetime', 'username_id')
	list_filter = ('id', 'question', 'answer', 'status', 'datetime', 'username_id')
	ordering = ('id', 'question', 'answer', 'status', 'datetime', 'username_id')