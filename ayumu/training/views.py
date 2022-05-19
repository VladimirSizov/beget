import re
from django.shortcuts import render
from .models import Translation, Result, Current, ENG, RUS
from .forms import InterviewForm
from django.http import HttpResponseRedirect
from .dict import Dict


# опрос
def interview(request):

	username_id = request.user.id
	words = Translation.words.all()
	id_word = get_id_current_word(request)
	word = words.get(id=id_word)
	question = word.eng

	# проверка предыдущий результат на правильный ответ
	previous_result = ''
	try:
		result = Result.objects.filter(username_id=username_id).latest('datetime')
		print(result)
		if result.status == True:
			# информирование пользователя о правильном ответе
			previous_result = 'ALL RIGHT!'
		if result.status == False:
			# найти правильные и показать
			arr_correct_answers = get_correct_answer(result.question)
			correct_answers = ''
			for element in arr_correct_answers:
				correct_answers += element + ', '
			previous_result = result.question + ' - ' + correct_answers[:-2]
	except:
		previous_result = ''
	# если пользователь отправляет ответ
	if request.method == 'POST':
		# полное обновление словаря ENG_RUS
		#upd_dict(request)
		# проверка на ошибки
		# test_dict()
		form = InterviewForm(request.POST)
		if form.is_valid():
			answer = form.cleaned_data['answer']
			status = False
			correct_answers = get_correct_answer(question)
			if answer in correct_answers:
				status = True
			result = Result(question=question, answer=answer, status=status, username_id=username_id)
			result.save()
			delete_current_word(request)
			return HttpResponseRedirect(request.path_info)
	else:
		form = InterviewForm()
		context = {'previous_result': previous_result, 'question': question, 'form': form}
		return render(request, 'training/interview.html', context)


# при неправильном ответе пользователя - получение правильных ответов, для строки пояснения
def get_correct_answer(question):
	arr = []
	eng = Translation.words.filter(eng=question)
	rus = Translation.words.filter(rus=question)
	for word in eng:
		arr.append(word.rus)
	for word in rus:
		arr.append(word.eng)
	return arr

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
		get_array_test(username_id)
		result = Current.objects.get(username_id=username_id)
		text = result.tested_words
		arr_words = re.findall('([-+]?\d+)', text)
	# достаем слово
	word = arr_words.pop()
	return word

# получаем id-слова для теста из временного хранилища
def delete_current_word(request):
	username_id = request.user.id
	result = Current.objects.get(username_id=username_id)
	text = result.tested_words
	arr_words = re.findall('([-+]?\d+)', text)
	word = arr_words.pop()
	result.tested_words = arr_words
	result.save()

# создаем новый массив тестов
def get_array_test(username_id):
	arr_words = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	current = Current.objects.get(username_id=username_id)
	current.tested_words = arr_words
	current.save()

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


