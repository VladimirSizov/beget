from django import forms


class LoginForm(forms.Form):
	""" форма авторизации пользователя """
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)