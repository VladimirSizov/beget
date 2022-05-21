from django import forms
from .models import Translation, Result


class InterviewForm(forms.Form):
	""" форма опроса """
	answer = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'autofocus': ''}))

