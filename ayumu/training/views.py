from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Result
from .forms import InterviewForm
from .inter import Interview, PreviousResult
from .create_data import CreateData # используется для полное обновление словаря ENG_RUS в CreateData.upd_dict()


# опрос
def interview(request):
	username_id = request.user.id
	# проверка предыдущий результат на правильный ответ
	previous_result = ''
	try:
		# получаем последний ответ
		result = Result.objects.filter(username_id=username_id).latest('datetime')
		if result.status == True:
			# информирование пользователя о правильном ответе
			previous_result = 'ALL RIGHT!'
		if result.status == False:
			# найти правильные и показать
			previous = PreviousResult(request)
			previous.test_type = result.test_type
			previous.question = result.question
			arr_correct_answers = previous.get_correct_answer()
			correct_answers = ''
			for element in arr_correct_answers:
				correct_answers += element + ', '
			previous_result = result.question + ' - ' + correct_answers[:-2]
	except:
		previous_result = ''
	# получаем слово для запроса
	interview = Interview(request)
	question = interview.get_current_word()  # слово для запроса
	# если пользователь отправляет ответ
	if request.method == 'POST':
		# полное обновление словаря ENG_RUS
		#CreateData.upd_dict()
		form = InterviewForm(request.POST)
		if form.is_valid():
			answer = form.cleaned_data['answer']
			status = False
			test_type = interview.test_type
			correct_answers = interview.get_correct_answer() # получаем список корректных ответов
			if answer in correct_answers:
				status = True
			result = Result(question=question, answer=answer, status=status, username_id=username_id, test_type=test_type)
			result.save()
			# корректируем параметры
			interview.correct_status()
			return HttpResponseRedirect(request.path_info)
	else:
		form = InterviewForm()
		context = {'previous_result': previous_result, 'question': question, 'form': form}
		return render(request, 'training/interview.html', context)

