from django.shortcuts import render
from django.http import HttpResponse
from .models import Translation


def interview(request):
	words = Translation.words.all()
	return render(request, 'training/interview.html', {'words': words})



