from django.shortcuts import render
from .models import Translation, Result
from .forms import InterviewForm
from django.http import HttpResponseRedirect


# опрос
def interview(request):
	words = Translation.words.all()
	word = words.get(id=3)

	question = word.eng

	# проверка предыдущий результат на правильный ответ
	previous_result = ''
	try:
		result = Result.objects.latest('datetime')
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
			username_id = request.user.id
			answer = form.cleaned_data['answer']
			status = False
			correct_answers = get_correct_answer(question)
			if answer in correct_answers:
				status = True
			result = Result(question=question, answer=answer, status=status, username_id=username_id)
			result.save()
			return HttpResponseRedirect(request.path_info)
	else:
		form = InterviewForm()
		return render(request, 'training/interview.html', {'previous_result': previous_result, 'question': question, 'form': form})


# при неправильном ответе пользователя - получение правильных ответов, для строки пояснения
def get_correct_answer(question):
	arr = []
	eng = Translation.words.filter(eng=question)
	rus = Translation.words.filter(rus=question)
	for word in eng:
		arr.append(word.rus)
	for word in rus:
		arr.append(word.eng)
	print(arr)
	return arr


