from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Result(models.Model):
	""" результаты тестов """
	TYPE_DICT = [('ER', 'ER'), ('RE', 'RE')]
	username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results') # 57
	answer = models.CharField(max_length=100)
	question = models.CharField(max_length=100)
	status = models.BooleanField(blank=False) # правильный ответ true/false
	test_type = models.CharField(max_length=2, choices=TYPE_DICT, default='ER')  # True = eng-rus
	datetime = models.DateTimeField(default=timezone.now)
	objects = models.Manager()


class Current(models.Model):
	""" текущие состояния пользователя """
	TYPE_DICT = [('ER', 'ER'), ('RE', 'RE')]
	username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='currents')
	tested_words = models.CharField(max_length=100, default=[])
	test_type = models.CharField(max_length=2, choices=TYPE_DICT, default='ER') # True = eng-rus
	type_increment = models.IntegerField(default=2) # обратный отчет попыток в этой языковой форме (ER или RE)
	last_word_eng = models.IntegerField(default=0, blank=True) # id последнее изученное слово ENG
	last_word_rus = models.IntegerField(default=0, blank=True) # id последнее изученное слово RUS
	objects = models.Manager()


class ENG(models.Model):
	""" слварь английских слов """
	eng = models.CharField(max_length=100, unique=True)
	objects = models.Manager()
	def __str__(self):
		return self.eng
	class Meta:
		ordering = ('eng',)


class RUS(models.Model):
	""" слварь русских слов """
	rus = models.CharField(max_length=100, unique=True)
	english = models.ManyToManyField(ENG)
	objects = models.Manager()
	def __str__(self):
		return self.rus
	class Meta:
		ordering = ('rus',)


class Lexicon(models.Model):
	""" статистика ответов тестирования """
	TYPE_DICT = [('ER', 'ER'), ('RE', 'RE')]
	word_id = models.IntegerField(default=0)
	word = models.CharField(max_length=100)
	results = models.CharField(max_length=100, default=[])
	percent = models.IntegerField(default=0)
	attempts = models.IntegerField(default=0)
	test_type = models.CharField(max_length=2, choices=TYPE_DICT, default='ER')  # True = eng-rus
	username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lexicon')
	objects = models.Manager()

