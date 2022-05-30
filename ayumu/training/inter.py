import re
from .models import Current, ENG, RUS, Lexicon
from .create_test import CreateTest


class StatAnsLex():
	""" статистика по ответам """

	def __init__(self, request):
		self.request = request
		self.user_id = request.user.id
		self.question = ''
		self.question_id = ''
		self.status = False
		self.results = []
		self.attempts = 0


	# получить id  для question
	def get_question_id(self):
		try:
			get_id = ENG.objects.get(eng=self.question).id
			self.question_id = get_id
		except:
			get_id = RUS.objects.get(rus=self.question).id
			self.question_id = get_id


	# получаем предыдущие результаты, или создаём НОВУЮ строку в Lexicon
	def check(self):
		try:
			lexicon = Lexicon.objects.filter(username_id=self.user_id).get(word=self.question).results
		except:
			self.get_question_id()
			lexicon = Lexicon(username_id=self.user_id, word=self.question, word_id=self.question_id)
			lexicon.save()
			lexicon = Lexicon.objects.filter(username_id=self.user_id).get(word=self.question).results
		return lexicon

	# получение старых результатов
	def update_results(self):
		results = self.check()
		results = re.findall('([-+]?\d+)', results)
		if self.status == True:
			results.append(1)
		else:
			results.append(0)
		self.results = results
		return results

	# обновления процента правильных ответов
	def update_percent(self):
		results = self.results # [-10:]
		attempts = len(results)
		if attempts == 0:
			percent = 0
		else:
			sum_i = 0
			for i in results:
				sum_i += int(i)
			percent = sum_i * 100 / attempts
			self.attempts = attempts
		return percent

	# сохранение в бд значений строк LEXICON
	def save_result(self):
		results = self.update_results()
		lexicon = Lexicon.objects.filter(username_id=self.user_id).get(word=self.question)
		lexicon.results = results
		lexicon.percent = self.update_percent()
		lexicon.attempts = self.attempts
		lexicon.test_type = Current.objects.get(username_id=self.user_id).test_type
		lexicon.save()



class PreviousResult():
	""" методы выведения данных предыдущего результата """

	def __init__(self, request):
		self.request = request
		self.user_id = request.user.id
		self.question = ''
		self.test_type = ''

	# получение правильного ответа на вопрос
	def get_correct_answer(self):
		arr = []
		if self.test_type == 'ER':
			# по англ ключу все знач рус
			eng_relation = ENG.objects.get(eng=self.question).rus_set.all()
			for word in eng_relation:
				arr.append(word.rus)
		if self.test_type == 'RE':
			# по рус ключу все знач англ
			rus_id = RUS.objects.get(rus=self.question).id
			rus_relation = ENG.objects.filter(rus__id=rus_id)
			for word in rus_relation:
				arr.append(word.eng)
		correct_answers = ''
		for element in arr:
			correct_answers += element + ', '
		return correct_answers[:-2]



class Interview():
	""" методы для обработки данных проведения опроса, записи в БД """

	def __init__(self, request):
		self.request = request
		self.user_id = request.user.id
		self.question = ''
		self.test_type = 'ER' # только для записи в Result

	# получаем слово для теста
	def get_current_word(self):
		# проверяем есть ли запись о пользователе, если нет создаем пустую
		try:
			Current.objects.get(username_id=self.user_id)
		except:
			new_user = Current(username_id=self.user_id)
			new_user.save()
		self.test_type = Current.objects.get(username_id=self.user_id).test_type
		word = ''
		word_id = self.get_id_current_word()
		# выбираем словарь
		if self.test_type == 'ER':
			word = ENG.objects.get(id=word_id).eng
		if self.test_type == 'RE':
			word = RUS.objects.get(id=word_id).rus
		self.question = word
		return word

	# получаем id-слова для теста
	def get_id_current_word(self):
		# пробуем получить слово для теста
		result = Current.objects.get(username_id=self.user_id)
		text = result.tested_words
		arr_words = re.findall('([-+]?\d+)', text)
		if len(arr_words) == 0:
			self.get_array_test() # создаем новый масссив с id слов для теста
			result = Current.objects.get(username_id=self.user_id)
			text = result.tested_words
			arr_words = re.findall('([-+]?\d+)', text)
		# достаем слово
		word = arr_words.pop()
		return word

	# удаляем использованное id-слова для теста из временного хранилища
	def correct_status(self):
		current = Current.objects.get(username_id=self.user_id)
		# откусываем id последнее слово
		tested_word = re.findall('([-+]?\d+)', current.tested_words)
		tested_word.pop()
		current.tested_words = tested_word
		current.save()

	# создаем новый массив тестов
	def get_array_test(self):
		# осталось раз для этого типа (ER или RE)
		type_increment = Current.objects.get(username_id=self.user_id).type_increment
		if type_increment == 0:
			current = Current.objects.get(username_id=self.user_id)
			# базовое количество подходов в одной языковой группе при смене языковой группы
			current.type_increment = 3 + 1
			test_type = Current.objects.get(username_id=self.user_id).test_type  # текущий тип тестирования
			# меняем язык
			if test_type == 'ER':
				current.test_type = 'RE'
			if test_type == 'RE':
				current.test_type  = 'ER'
			# сохраняем
			current.save()
		# добавляем новые слова и сохраняем
		test_type = Current.objects.get(username_id=self.user_id).test_type
		create_test = CreateTest(self.request, test_type)
		tested_words = create_test.get_id_words()
		current = Current.objects.get(username_id=self.user_id)
		current.tested_words = tested_words
		current.type_increment -= 1
		current.save()

	# при неправильном ответе пользователя - получение правильных ответов, для строки пояснения
	def get_correct_answer(self):
		arr = []
		if self.test_type == 'ER':
			# по англ ключу все знач рус
			eng_relation = ENG.objects.get(eng=self.question).rus_set.all()
			for word in eng_relation:
				arr.append(word.rus)
		if self.test_type == 'RE':
			# по рус ключу все знач англ
			rus_id = RUS.objects.get(rus=self.question).id
			rus_relation = ENG.objects.filter(rus__id=rus_id)
			for word in rus_relation:
				arr.append(word.eng)
		return arr


class CheckResponse():
	""" методы для обработки данных проведения опроса, записи в БД """

	def __init__(self, request, wrong):
		self.request = request
		self.wrong = wrong

	# при неправильном ответе пользователя - получение правильных ответов, для строки пояснения
	def get_values(self):
		arr = []
		try:
			# по англ ключу все знач рус
			eng_relation = ENG.objects.get(eng=self.wrong).rus_set.all()
			for word in eng_relation:
				arr.append(word.rus)
		except:
			# по рус ключу все знач англ
			rus_id = RUS.objects.get(rus=self.wrong).id
			rus_relation = ENG.objects.filter(rus__id=rus_id)
			for word in rus_relation:
				arr.append(word.eng)
		correct_answers = ''
		for element in arr:
			correct_answers += element + ', '
		return correct_answers[:-2]




	#################################################

	# получаем слово для теста
	def get_current_word(self):
		# проверяем есть ли запись о пользователе, если нет создаем пустую
		try:
			Current.objects.get(username_id=self.user_id)
		except:
			new_user = Current(username_id=self.user_id)
			new_user.save()
		self.test_type = Current.objects.get(username_id=self.user_id).test_type
		word = ''
		word_id = self.get_id_current_word()
		# выбираем словарь
		if self.test_type == 'ER':
			word = ENG.objects.get(id=word_id).eng
		if self.test_type == 'RE':
			word = RUS.objects.get(id=word_id).rus
		self.question = word
		return word

	# получаем id-слова для теста
	def get_id_current_word(self):
		# пробуем получить слово для теста
		result = Current.objects.get(username_id=self.user_id)
		text = result.tested_words
		arr_words = re.findall('([-+]?\d+)', text)
		if len(arr_words) == 0:
			self.get_array_test() # создаем новый масссив с id слов для теста
			result = Current.objects.get(username_id=self.user_id)
			text = result.tested_words
			arr_words = re.findall('([-+]?\d+)', text)
		# достаем слово
		word = arr_words.pop()
		return word

	# удаляем использованное id-слова для теста из временного хранилища
	def correct_status(self):
		current = Current.objects.get(username_id=self.user_id)
		# откусываем id последнее слово
		tested_word = re.findall('([-+]?\d+)', current.tested_words)
		tested_word.pop()
		current.tested_words = tested_word
		current.save()

	# создаем новый массив тестов
	def get_array_test(self):
		# осталось раз для этого типа (ER или RE)
		type_increment = Current.objects.get(username_id=self.user_id).type_increment
		if type_increment == 0:
			current = Current.objects.get(username_id=self.user_id)
			# базовое количество подходов в одной языковой группе при смене языковой группы
			current.type_increment = 3 + 1
			test_type = Current.objects.get(username_id=self.user_id).test_type  # текущий тип тестирования
			# меняем язык
			if test_type == 'ER':
				current.test_type = 'RE'
			if test_type == 'RE':
				current.test_type  = 'ER'
			# сохраняем
			current.save()
		# добавляем новые слова и сохраняем
		test_type = Current.objects.get(username_id=self.user_id).test_type
		create_test = CreateTest(self.request, test_type)
		tested_words = create_test.get_id_words()
		current = Current.objects.get(username_id=self.user_id)
		current.tested_words = tested_words
		current.type_increment -= 1
		current.save()
