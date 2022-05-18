from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
	""" форма авторизации пользователя """
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
	""" форма регистрации нового пользователя """
	#date_of_birth
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

	# создание нового пользователя в БД
	class Meta:
		model = User
		fields = ('username', 'first_name', 'email')

	# метод типа <clean_> проверка на совпадение, здесь паролей
	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError("Passwords don't match.")
		return cd['password2']