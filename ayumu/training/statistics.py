from .models import Result, Lexicon
from datetime import datetime, timedelta


class Statistics():
	""" статистика результатов пользователя """

	def __init__(self, request):
		self.request = request
		self.user_id = request.user.id
		self.data_results = []
		self.data_lexicon = []


	# самые трудные слова
	def most_difficult(self):
		self.get_lexicon()
		if self.data_lexicon:
			result = self.data_lexicon.filter(test_type='ER').order_by('percent')[:11]
			arr = []
			for i in result:
				arr.append(i.word)
			return arr


	# процент ошибок в ответах
	def get_percentage_correct_answer(self):
		self.get_result()
		all = len(self.data_results)
		if all > 0:
			right = len(Result.objects.filter(username_id=self.user_id).filter(status=True))
			percent = int(100 - (right * 100 / all))
			return percent
		return 0

	# изученных слов всего
	def get_learned_words(self):
		self.most_difficult()
		# определяем время за последние сутки
		today = datetime.today()
		day = today - timedelta(hours=23, minutes=59, seconds=59)
		day = day.date()
		# всего уникальных по 'question'
		all_learned_words = len(Result.objects.filter(username_id=self.user_id, test_type='ER').values('question').distinct())
		# за сутки уникальных по 'question'
		learned_words_today = len(Result.objects.filter(username_id=self.user_id, test_type='ER', datetime__gt=day).values('question').distinct())
		return {'all_w': all_learned_words, 'today_w': learned_words_today}

	# попыток
	def get_try(self):
		if Result.objects.filter(username_id=self.user_id):
			return len(Result.objects.filter(username_id=self.user_id))
		return 0

	# получить данные результатов
	def get_result(self):
		self.data_results = Result.objects.filter(username_id=self.user_id)

	def get_lexicon(self):
		self.data_lexicon = Lexicon.objects.filter(username_id=self.user_id)

