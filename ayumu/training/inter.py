import re
from .models import Current, ENG, RUS, Lexicon
from .create_test import CreateTest


class StatAnsLex():
	""" статистика по ответам """

	def __init__(self, request):
		self.request = request
		self.user_id = request.user.id
		self.question = ''
		self.status = False
		self.results = []
		self.attempts = 0

	# получаем предыдущие результаты,
	def check(self):
		try:
			lexicon = Lexicon.objects.filter(username_id=self.user_id).get(word=self.question).results
		except:
			lexicon = Lexicon(username_id=self.user_id, word=self.question)
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

	# сохранение в бд
	def save_result(self):
		results = self.update_results()
		lexicon = Lexicon.objects.filter(username_id=self.user_id).get(word=self.question)
		lexicon.results = results
		lexicon.percent = self.update_percent()
		lexicon.attempts = self.attempts
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
		return arr



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
		current = Current.objects.get(username_id=self.user_id)
		# осталось раз для этого типа (ER или RE)
		type_increment = Current.objects.get(username_id=self.user_id).type_increment
		print('type_increment')
		print(type_increment)
		test_type = ''
		if type_increment == 0:
			# базовое количество подходов в одной языковой группе при смене языковой группы
			current.type_increment = 1 + 1
			test_type = Current.objects.get(username_id=self.user_id).test_type  # текущий тип тестирования
			print('test_type')
			print(test_type)
			# меняем язык
			if test_type == 'ER':
				current.test_type = 'RE'
				print('test_type')
				print(test_type)
			if test_type == 'RE':
				current.test_type  = 'ER'
				print('test_type')
				print(test_type)
		create_test = CreateTest(test_type)
		tested_words = create_test.get_id_words()
		current.type_increment -= 1
		current.tested_words = tested_words
		# сохраняем
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


"""
# по АНГ id - РУС значения
i = RUS.objects.filter(english__id=5)
# по АНГ id - АНГ значения
i = ENG.objects.filter(id=1)

# все РУС слова, в АНГ значениях которых есть 'be'
i = RUS.objects.filter(english__eng__startswith='be')
# все АНГ слова, включает буковку 'в'
i = ENG.objects.filter(rus__rus__startswith='в')
# по РУС id - АНГ значения
i = ENG.objects.filter(rus__id=5)

i = RUS.objects.filter(rus='из').get()
"""

