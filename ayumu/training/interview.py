# методы для обработки данных проведения опроса, записи в БД

class Interview():
	"""  """
	def __init__(self, request, question):
		self.request = request

	# при неправильном ответе пользователя - получение правильных ответов, для строки пояснения
	def get_correct_answer(request, question):
		username_id = request.user.id
		test_type = Current.objects.get(username_id=username_id).test_type
		arr = []
		if test_type == 'ER':
			# по англ ключу все знач рус
			eng_relation = ENG.objects.get(eng=question).rus_set.all()
			for word in eng_relation:
				arr.append(word.rus)
		if test_type == 'RE':
			# по рус ключу все знач англ
			rus_relation = ENG.objects.filter(rus=question)
			for word in rus_relation:
				arr.append(word.eng)
		return arr


	# получаем слово для теста
	def get_current_word(request):
		username_id = request.user.id
		test_type = Current.objects.get(username_id=username_id).test_type
		word = ''
		word_id = get_id_current_word(request)
		# выбираем словарь
		if test_type == 'ER':
			word = ENG.objects.get(id=word_id).eng
		if test_type == 'RE':
			word = RUS.objects.get(id=word_id).rus
		return word


	# получаем id-слова для теста
	def get_id_current_word(request):
		username_id = request.user.id
		# проверяем есть ли запись о пользователе, если нет создаем пустую
		try:
			Current.objects.get(username_id=username_id)
		except:
			new_user = Current(tested_words=[], username_id=username_id)
			new_user.save()
		# пробуем получить слово для теста
		result = Current.objects.get(username_id=username_id)
		text = result.tested_words
		arr_words = re.findall('([-+]?\d+)', text)
		if len(arr_words) == 0:
			get_array_test(request) # создаем новый масссив с id слов для теста
			result = Current.objects.get(username_id=username_id)
			text = result.tested_words
			arr_words = re.findall('([-+]?\d+)', text)
		# достаем слово
		word = arr_words.pop()
		return word

	# удаляем использованное id-слова для теста из временного хранилища
	def delete_current_word(request):
		username_id = request.user.id
		result = Current.objects.get(username_id=username_id) # это обязательно?
		text = result.tested_words
		arr_words = re.findall('([-+]?\d+)', text)
		word = arr_words.pop()
		result.tested_words = arr_words
		result.save()

	# создаем новый массив тестов
	def get_array_test(request):
		username_id = request.user.id
		type_increment = Current.objects.get(username_id=username_id).type_increment # осталось раз для этого типа (ER или RE)
		test_type = Current.objects.get(username_id=username_id).test_type # текущий тип тестирования

		arr_words = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		current = Current.objects.get(username_id=username_id)
		current.tested_words = arr_words
		current.save()


	#######################################################
	# заполняем словари словами
	def upd_dict(request):
		all_words = [Dict.d_1_1000, Dict.d_1001_2000, Dict.d_2001_3000, Dict.d_3001_4000, Dict.d_4001_5000]
		for words in all_words:
			for word in words:
				for rus in word[1]:
					eng = ENG(eng=word[0])
					# проверяем ENG что слова еще нет в словаре
					try:
						ENG.objects.get(eng=eng)
					except:
						# если ENG нет - то добавляем
						eng.save()
					eng_id = ENG.objects.get(eng=eng).id

					rus = RUS(rus=rus)
					# проверяем RUS что слова еще нет в словаре
					try:
						RUS.objects.get(rus=rus)
					except:
						# если RUS нет - то добавляем
						rus.save()
					rus_value = RUS.objects.get(rus=rus)
					# добавляем связь многие ко многим
					rus_value.english.add(eng_id)


	def test_dict():
		# запросы к БД тестирование на ошибки
		id_eng = 8
		id_rus = 6
		# по англ ключу все знач рус
		eng_relation = ENG.objects.get(id=id_eng).rus_set.all()
		print(eng_relation)
		# по рус ключу все знач англ
		rus_relation =ENG.objects.filter(rus__id=id_rus)
		print(rus_relation)



