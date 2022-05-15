from django.contrib import admin
from .models import Translation


@admin.register(Translation)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('id', 'eng', 'rus')
	ordering = ('id', 'eng', 'rus')
