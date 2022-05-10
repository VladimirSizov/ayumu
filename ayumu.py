from autorization import AuthUser
from statistics import Statistics
from create_test import CreateTest
from interview import Interview
from settings import Settings


def ayumu():
	"""основной цикл программы"""
	# инициализация настроек
	ay_settings = Settings()
	# авторизация пользователя, и выбор тренировки
	user = AuthUser()
	user.auth_user()
	base_adress = user.base_adress
	language_type = user.language_type
	# проверяем базу предыдущих ответов на наличие исключений
	base_test = CreateTest(base_adress, language_type)
	base_test.base_check()
	# результаты статистики
	stat = Statistics(base_adress, ay_settings.percent_know)
	stat.previous_results()
	# запускаем основной цикл, опрос
	flag = True
	while flag:
		# создаём список слов для теста
		create_new_test = CreateTest(base_adress, language_type)
		new_test = create_new_test.arrangement()
		old_result = create_new_test.extract_dict_result()
		dict_with_value = create_new_test.extract_dict_values_all()
		# опрашиваем
		# print('ups!')
		new_interview = Interview(new_test, old_result, dict_with_value, language_type, base_adress)
		new_interview.testing()


# flag = False
ayumu()
