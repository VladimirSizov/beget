from .models import Result

class Statistics():
	""" статистика результатов пользователя """

	def __init__(self, request):
		self.request = request
		self.user_id = request.user.id
		self.data_results = []


	# процент правильных ответов
	def get_percentage_correct_answer(self):
		self.get_result()
		all = len(self.data_results)
		if all > 0:
			right = len(Result.objects.filter(username_id=self.user_id).filter(status=True))
			percent = int(right * 100 / all)
			print("true percent: " + str(percent))
			return percent
		return 0


	# получить данные результатов
	def get_result(self):
		self.data_results = Result.objects.filter(username_id=self.user_id)

