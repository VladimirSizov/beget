from django.shortcuts import render
from .models import Translation, Result
from .forms import InterviewForm
from django.http import HttpResponseRedirect



# опрос
def interview(request):
	words = Translation.words.all()
	word = words.get(id=1)
	print(word)

	question = word.eng

	if request.method == 'POST':
		form = InterviewForm(request.POST)
		if form.is_valid():
			username_id = request.user.id
			answer = form.cleaned_data['answer']
			control_answer = word.rus
			status = False
			if answer == control_answer:
				status = True
			result = Result(question=question, answer=answer, status=status, username_id=username_id)
			result.save()
			return HttpResponseRedirect(request.path_info)
	else:
		form = InterviewForm()
		return render(request, 'training/interview.html', {'question': question, 'form': form})
	# return render(request, 'training/interview.html', {'word': word})



