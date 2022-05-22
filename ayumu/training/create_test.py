import re
from .models import Current, ENG, RUS, Lexicon

class CreateTest():
	""" методы для тестирования """

	def __init__(self, test_type):
		self.test_type = test_type
		self.extract_dict_result = [] #заменить на него
		self.test_dictionary = [1, 2, 3] # заменить на []



	# получить новые id слов для теста
	def get_id_words(self):


		return self.test_dictionary

	# получить новые слова
	def dict_word_new(self):
		print("")

	# показать количество слов, ниже определённого показателя % правильных ответов
	def rate_percent(self, percent):

		data_old_result = self.extract_dict_result()
		if data_old_result:
			low_percent = []
			for word in data_old_result:
				if word[3] < percent:
					low_percent.append(word)
			if low_percent:
				return (len(low_percent))
		return 0

	def extract_dict_result(self):
		self.extract_dict_result = Lexicon.objects.all()


