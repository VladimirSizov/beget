from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Result
from .forms import InterviewForm
from .inter import Interview, PreviousResult, StatAnsLex, CheckResponse
from .statistics import Statistics
from .create_data import CreateData # используется для полное обновление словаря ENG_RUS в CreateData.upd_dict()


# опрос
def interview(request):
	username_id = request.user.id
	# статистика
	all_w = Statistics(request).get_learned_words()['all_w']
	today_w = Statistics(request).get_learned_words()['today_w']
	true_percent = Statistics(request).get_percentage_correct_answer() # процент правильн ответов
	get_try = Statistics(request).get_try()

	# проверка предыдущий результат на правильный ответ
	previous_result = ''
	wrong_answers_result = ''
	try:
		# получаем последний ответ
		result = Result.objects.filter(username_id=username_id).latest('datetime')
		if result.status == True:
			# информирование пользователя о правильном ответе
			previous_result = '' # строка текста при правильном ответе, заполнить типа: "молодец, продолжай!"
		if result.status == False:
			# найти и показать у неправильного ответа его правильные значения

		
			wrong = result.answer
			value_wrong = CheckResponse(request, wrong)
			try:
				answer_words = value_wrong.get_values()
				wrong_answers_result = wrong + ' - ' + answer_words
			except:
				wrong_answers_result = ''


			# найти правильные и показать правильные значения
			previous = PreviousResult(request)
			previous.test_type = result.test_type
			previous.question = result.question
			c_answers = previous.get_correct_answer()
			previous_result = result.question + ' - ' + c_answers
	except:
		previous_result = ''
	# получаем слово для запроса
	interview = Interview(request)
	question = interview.get_current_word() # слово для запроса
	print("question: " + str(question))
	# если пользователь отправляет ответ
	if request.method == 'POST':
		# полное обновление словаря ENG_RUS
		#CreateData.upd_dict()
		form = InterviewForm(request.POST)
		if form.is_valid():
			answer = form.cleaned_data['answer']
			print('answer: ' + str(answer))
			status = False
			test_type = interview.test_type
			correct_answers = interview.get_correct_answer() # получаем список корректных ответов
			if answer in correct_answers:
				status = True
			# прописываем статистику
			lex_stat = StatAnsLex(request)
			lex_stat.status = status
			lex_stat.question = question
			lex_stat.save_result()
			# сохраняем результаты ответов
			result = Result(question=question, answer=answer, status=status, username_id=username_id, test_type=test_type)
			result.save()
			# корректируем параметры
			interview.correct_status()
			return HttpResponseRedirect(request.path_info)
	else:
		form = InterviewForm()
		context = {'get_try': get_try, 'wrong_answers_result': wrong_answers_result, 'today_w': today_w, 'all_w': all_w, 'true_percent': true_percent, 'previous_result': previous_result, 'question': question, 'form': form}
		return render(request, 'training/interview.html', context)

