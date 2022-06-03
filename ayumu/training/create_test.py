# -----NEW
# НОВЫЕ СЛОВА изначальный показатель 50/50% (правильные/неправильные)
# слово, значение которого пользователь ранее не вводил
# / добавляютя при при наличии старых результатах до 20 слов с показателем менее 50%

# -----LO%
# ПЛОХИЕ РЕЗУЛЬТАТЫ
# слово с самым низким показателем качества ответов (правильные/неправильные)
# / добавляется всегда

# -----BEG
# НОВИЧОК мало изученное, не набравшее статистики
# слово, которое показывалось менее 5-ти раз
# / добавляется всегда

# -----OLD
# РАНДОМНЫЕ СТАРЫЕ
# слово которые уже показывались ранее
# / добавляютя при при наличии старых результатах до 20 слов с показателем менее 50%

# -----BLSH
# чтото среднее между LO% и BEG
# слово, самые низкие показатели правильных_ответов/количеству показов на индекс ответов до [8]
# / добавляютя при при наличии старых результатах до 20 слов с показателем менее 50%

# -----------------
# возможно в функции arrangement стоит добавить условия запуска вложенных функций


import re
import random
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
			if self.index_min_percent(24, 71):
				self.dict_word_new()
			if self.index_min_percent(26, 81):
				self.dict_word_new()
			# добавляем малоизученные слова BEGINER
			self.word_small_views()
			# добавляем известные слова
			for i in range(1, int(self.len_old_result()/500+1)):
				self.dict_word_old_random()
			# добавляем слово, самые низкие показатели правильных_ответов/количеству показов
				self.black_sheep()
			# добавляем мало изученные слова
			self.dict_word_low_percent()

		print('self.test_dictionary')
		print(self.test_dictionary)
		return self.test_dictionary

	# получить новые слова
	def dict_word_new(self):
		# получаем id слова в зависимости от режима тренировки
		flag = False
		id_new_word = self.increase_id_new_word()
		if self.test_type == 'ER':
			if ENG.objects.get(id=id_new_word):
				flag = True
		if self.test_type == 'RE':
			if RUS.objects.get(id=id_new_word):
				flag = True
		# если слово с этим id существует (самое большое например нет)
		if flag:
			# проверка хреновых показателей ;)
			# self.rate_percent(61)
			# узнаем количество малоизученных
			# при условии добавляем новое слово в тест
			a = self.index_min_percent(22, 61)
			if a:
				b = self.index_min_percent(20, 51)
				#print('b')
				#print(b)
				if a and b:
					if id_new_word not in self.test_dictionary:
						self.test_dictionary.append(id_new_word)
						print('-----NEW')
						print(id_new_word)
			# первый запуск
			if len(self.extract_dict_result) < 10:
				if id_new_word not in self.test_dictionary:
					self.test_dictionary.append(id_new_word)
					print('-----NEW_NEW')
					print(id_new_word)

	# подбор слов с низким %
	def dict_word_low_percent(self):
		if self.extract_dict_result:
			id_new_word = self.extract_dict_result.order_by('percent')[0].word_id
			if id_new_word not in self.test_dictionary:
				self.test_dictionary.append(id_new_word)
				print('-----LO%')
				print(id_new_word)

	# новичок
	def word_small_views(self):
		new_word = self.index_min_view_percent(4, 100)
		if new_word:
			if new_word not in self.test_dictionary:
				self.test_dictionary.append(new_word)
				print('-----BEG')
				print(new_word)

	# подбор слов старых(временная функция - для теста)
	def dict_word_old_random(self):
		data_rate = self.index_min_percent(20, 51)
		if data_rate:
			data_old_result = self.extract_dict_result
			if data_old_result:
				index = random.randint(0, len(data_old_result) - 1)
				new_word = data_old_result[index].word_id
				if new_word not in self.test_dictionary:
					self.test_dictionary.append(new_word)
					print('-----OLD')
					print(new_word)

	# слово, самые низкие показатели правильных_ответов/количеству показов
	def black_sheep(self):
		data_old_result = self.extract_dict_result
		if data_old_result and len(data_old_result) > 5:
			# отбираем 10% худших
			rate = int(len(data_old_result) * 0.5)
			slice_attempts = data_old_result.order_by('attempts')[:rate]
			arr_low_attempts = []
			for word in slice_attempts:
				arr_low_attempts.append(word.word_id)
			slice_percent = data_old_result.order_by('percent')[:rate]
			arr_low_percent = []
			for word in slice_percent:
				arr_low_percent.append(word.word_id)
			# выбираем самый душный
			bad_result = []
			for word in arr_low_attempts:
				if word in arr_low_percent:
					bad_result.append(word)
			if bad_result:
				index = random.randint(0, len(bad_result) - 1)
				new_word = bad_result[index]
				if new_word not in self.test_dictionary:
					self.test_dictionary.append(new_word)
					print('-----BLSH')
					print(new_word)

	# __________________вспомогательные_____________________

	# количество слов протестированных
	def len_old_result(self):
		data = self.extract_dict_result
		if data:
			len_data = len(data)
		else:
			len_data = 0
		return len_data

	# показать количество слов, ниже определённого показателя % правильных ответов
	def rate_percent(self, percent):
		if self.extract_dict_result:
			low_percent = len(self.extract_dict_result.filter(percent__lt=percent).all())
			return low_percent
		return 0

	# подбор слов со значениями меньше заданных показателей:
	# количества_показов, процент_правильных_ответов
	def index_min_view_percent(self, view, percent):
		if self.extract_dict_result:
			data_old_result = self.extract_dict_result.filter(attempts__lt=view, percent__lt=percent)
			words = []
			for word in data_old_result:
				words.append(word.word_id)
			if words:
				index = random.randint(0, len(words) - 1)
				new_word = words[index]
				return new_word

	# увеличивает значение id нового слова, и сохраняем в Current
	def increase_id_new_word(self):
		id_new_word = 0
		new_data = Current.objects.get(username_id=self.user_id)
		if self.test_type == 'ER':
			new_data.last_word_eng = Current.objects.get(username_id=self.user_id).last_word_eng + 1
			new_data.save()
			id_new_word = Current.objects.get(username_id=self.user_id).last_word_eng
		if self.test_type == 'RE':
			new_data.last_word_rus = Current.objects.get(username_id=self.user_id).last_word_rus + 1
			new_data.save()
			id_new_word = Current.objects.get(username_id=self.user_id).last_word_rus
		return id_new_word

	# допуск, макс кол-ва слов с определённым показателем % правильных ответов
	def index_min_percent(self, max_amount, percent):
		if self.extract_dict_result:
			low_percent = len(self.extract_dict_result.filter(percent__lt=percent).all())
			if low_percent < max_amount:
				return True
			else:
				return False

	#__________________базовые_____________________

	# заполняем атрибут из QuerySet: self.extract_dict_result
	def extract_objects_result(self):
		self.test_type = Current.objects.get(username_id=self.user_id).test_type
		self.extract_dict_result = Lexicon.objects.filter(username_id=self.user_id, test_type=self.test_type)

