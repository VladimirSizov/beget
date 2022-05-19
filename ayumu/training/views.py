import re
from django.shortcuts import render
from .models import Translation, Result, Current
from .forms import InterviewForm
from django.http import HttpResponseRedirect


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
	arr_words = [1, 2, 3, 4, 5]
	current = Current.objects.get(username_id=username_id)
	current.tested_words = arr_words
	current.save()

