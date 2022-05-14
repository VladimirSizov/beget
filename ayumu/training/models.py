from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Translation(models.Model):
	""" таблица значений слов """
	eng = models.CharField(max_length=100)
	rus = models.CharField(max_length=100)

	def __str__(self):
		return self.eng
