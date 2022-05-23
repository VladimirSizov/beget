import re
from .models import Current, ENG, RUS, Lexicon

class CreateTest():
	"""создание и заполнение теста"""

	def __init__(self, request, test_type):
		self.request = request
		self.user_id = request.user.id
		self.test_type = test_type
		self.extract_dict_result = []
		self.test_dictionary = [] # заменить на []



	# получить новые id слов для теста
	def get_id_words(self):
		self.extract_objects_result() # заполняем атрибут из QuerySet: self.extract_dict_result
		# проверка количества слов с низким качеством ответов
		# print(self.rate_percent(61))
		if self.rate_percent(61) > 24:
			# print(self.rate_percent(61))
			# добавляем мало изученные слова
			self.dict_word_low_percent()
		else:
			# добавляем новые слова
			self.dict_word_new()
			# добавляем мало изученные слова
			self.dict_word_low_percent()

		print(self.test_dictionary)
		return self.test_dictionary



	# заполняем атрибут из QuerySet: self.extract_dict_result
	def extract_objects_result(self):
		self.extract_dict_result = Lexicon.objects.filter(username_id=self.user_id)


	# показать количество слов, ниже определённого показателя % правильных ответов
	def rate_percent(self, percent):
		if self.extract_dict_result:
			low_percent = len(self.extract_dict_result.filter(percent__lt=percent).all())
			return low_percent
		return 0


	# подбор слов с низким %
	def dict_word_low_percent(self):
		if self.extract_dict_result:
			id_new_word = self.extract_dict_result.order_by('percent')[0].id
			# print(new_word)
			if id_new_word not in self.test_dictionary:
				self.test_dictionary.append(id_new_word)
			print('-----LO%')
			print(id_new_word)


	# получить новые слова
	def dict_word_new(self):
		# получаем id слова в зависимости от режима тренировки
		flag = False
		id_new_word = 0
		if self.test_type == 'ER':
			id_new_word = Current.objects.get(username_id=self.user_id).last_word_eng + 1
			if ENG.objects.get(id=id_new_word):
				flag = True
		if self.test_type == 'RE':
			id_new_word = Current.objects.get(username_id=self.user_id).last_word_rus + 1
			if RUS.objects.get(id=id_new_word):
				flag = True
		# если слово с этим id существует (самое большое например)
		if flag:
			# проверка хреновых показателей ;)
			# self.rate_percent(61)
			# узнаем количество малоизученных
			# при условии добавляем новое слово в тест
			a = self.index_min_percent(22, 61)
			if a:
				b = self.index_min_percent(20, 51)
				if a and b:
					if id_new_word not in self.test_dictionary:
						self.test_dictionary.append(id_new_word)
						print('-----NEW')
						print(id_new_word)


	# допуск, макс кол-ва слов с определённым показателем % правильных ответов
	def index_min_percent(self, max_amount, percent):
		if self.extract_dict_result:
			low_percent = len(self.extract_dict_result.filter(percent__lt=percent).all())
			# print(low_percent)
			if low_percent < max_amount:
				return True
			else:
				return False





##########################
"""

	i = Lexicon.objects.filter(username_id='17')
	i = len(i.filter(percent__gt=70).all())
	print(len(i))



"""