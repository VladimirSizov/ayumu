import json


class AuthUser():
	def __init__(self):
		'''авторизация пользователя'''
		self.login_user = 'none'
		self.file_adress = 'none'
		self.base_adress = 'none'
		self.language_type = 'none'

	def name_file_adress(self):
		self.file_adress = 'auth/' + self.login_user.lower() + '.json'

	def auth_user(self):
		'''попытка входа, проверка наличия пользователя'''
		print('\nПожалуйста авторизуйтесь:')
		self.login_user = input('Логин: ')
		self.name_file_adress()
		try:
			self.verif_user(self.file_adress)
		except:
			ask_try = '\nЛогина "' + self.login_user + '" не существует. Что будем делать?\n\t- попытаемся ещё раз? (наберите "try" и нажмите Ввод)\n\t- создадим нового пользователя. (нажмите Ввод)\nОтвет: '
			answer_try = input(ask_try)
			if answer_try == 'try':
				self.auth_user()
			else:
				self.new_user()

	def new_user(self):
		'''создание нового профиля пользователя: верификация, словари ответов'''
		message = '\nСоздаём нового пользователя c логином "' + self.login_user + '" :'
		print(message)
		self.name_file_adress()
		password_user = input('Пароль: ')
		with open(self.file_adress, 'w') as obj:
			json.dump(password_user, obj)
		# здесь должны создаваться словари пользователя
		self.new_dictionaries()
		self.auth_user()

	def verif_user(self, file_adress):
		'''верификация пользователя'''
		with open(self.file_adress, 'r') as obj:
			verification = json.load(obj)
			password_user = input('Пароль: ')
			if password_user == verification:
				self.type_training()
				self.hello()
			else:
				print('Не верный пароль. Попробеум ещё.')
				self.auth_user()

	def new_dictionaries(self):
		'''создание словарей: ответы, статистика'''
		type_languages = ['eng-rus', 'rus-eng']
		# создаем шаблоны под ответы
		type_result = type_languages[:]
		while type_result:
			name_newuser_dict = type_result.pop()
			base_adress = 'user_result/' + self.login_user + '.' + name_newuser_dict + '.result.json'
			with open(base_adress, 'w') as obj:
				start = []
				json.dump(start, obj)
		# создаем шаблоны под статистику
		type_stat = type_languages[:]
		while type_stat:
			name_newuser_dict = type_stat.pop()
			base_adress = 'stat/' + self.login_user + '.' + name_newuser_dict + '.stat.json'
			with open(base_adress, 'w') as obj:
				start = [[0, 0]]
				json.dump(start, obj)

	def type_training(self):
		'''выбираем тип тренировки'''
		lang = input('\nВыберите тип тренировки (введите число):\nангло-русский - "1", русско-английский - "2": ')
		if int(lang) == 1:
			selected_type = 'eng-rus'
		else:
			selected_type = 'rus-eng'
		self.language_type = selected_type
		self.base_adress = 'user_result/' + self.login_user + '.' + selected_type + '.result.json'

	def hello(self):
		'''пролог'''
		print('\n---')
		print(
			'\n«Словарь Вильяма Шекспира, по подсчету исследователей, составляет 12 000 слов.\nСловарь негра из людоедского племени Мумбо-Юмбо составляет 300 слов.\nЭллочка Щукина легко и свободно обходилась тридцатью.»\nДвенадцать стульев. И.Ильф Е.Петров\n')
		print(
			'Ayumu(Аюми) - имя шимпанзе, который способен мгновенно запомнить и затем воспроизвести порядок и место расположения на мониторе чисел от 1 до 9.\n')
		print('---')
