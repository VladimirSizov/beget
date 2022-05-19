from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class WordsManager(models.Manager):
	""" менеджер QuerySet для words """
	def get_queryset(self):
		return super().get_queryset()


class Translation(models.Model):
	""" таблица значений слов """
	eng = models.CharField(max_length=100)
	rus = models.CharField(max_length=100)
	objects = models.Manager() # менеджер QuerySet по умолч
	words = WordsManager() # менеджер QuerySet наш
	def __str__(self):
		return self.eng


class Result(models.Model):
	""" результаты тестов """
	username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results') # 57
	answer = models.CharField(max_length=100)
	question = models.CharField(max_length=100)
	status = models.BooleanField(blank=False) # правильный ответ true/false
	datetime = models.DateTimeField(default=timezone.now)
	objects = models.Manager()


class Current(models.Model):
	""" текущие состояния пользователя """
	username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='currents')
	tested_words = models.CharField(max_length=100)
	objects = models.Manager()


class ENG(models.Model):
	""" слварь английских слов """
	eng = models.CharField(max_length=100)
	objects = models.Manager()
	def __str__(self):
		return self.eng
	class Meta:
		ordering = ('eng',)

class RUS(models.Model):
	""" слварь русских слов """
	rus = models.CharField(max_length=100)
	english = models.ManyToManyField(ENG)
	objects = models.Manager()
	def __str__(self):
		return self.rus
	class Meta:
		ordering = ('rus',)


