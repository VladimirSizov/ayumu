# В случае неправильного ответа, слово которое было введено в качестве ответа - 
# нужно также защитать неправильным, например 'нами':
# 	нами - 
# пользователь заполнил 'our',  и получил:
# 	нами - our
# 		our - наш, наши, наша, наше
# 		нами - us
# пользователь ю нужно засчитать минус балл и в 'нами' и в 'our'

import json


class Interview():
	"""опрос"""

	def __init__(self, new_test, old_result, dict_with_values_all, language_type, base_adress):
		# список слов для текущего теста
		self.for_test = new_test
		# список данных с предыдущими результатами
		self.old_result = old_result
		# текущий словарь с переводами
		self.dict_with_values_all = dict_with_values_all
		# тип перевода (eng-rus, rus-eng)
		self.language = language_type
		# результаты предыдущих опросов
		self.base_adress = base_adress

		# нов результаты, сырые
		self.result_test = []
		# нов результаты, добавленные к предыд результ, и готовые к записи
		self.result_test_add_old = []
		# нов результаты, с пересчитаные показателями
		self.result_data = []

	def testing(self):
		"""основной цикл опроса"""
		# тестирование
		self.new_respone()
		# вписываем новые результаты в старые
		self.rewrite_result()
		# пересчитываем параметры
		self.recalc_indicators()
		# записываем в файл
		self.json_dump()

	def new_respone(self):
		"""опрос"""
		result_test = []
		for_test = self.for_test
		while for_test:
			current = for_test.pop()
			# print('начали тест')
			# print(current)
			key_ask = current[0]
			# находим в словаре по ключу значения ответов
			for word in self.dict_with_values_all:

				if word[0] == key_ask:
					# спрашиваем и записываем результаты
					answer = input(str(key_ask) + ' - ')

					# если ответ правильный
					if answer in word[1]:
						y = int(current[1]) + 1
						del current[1]
						current.insert(1, y)
						result_test.append(current)
					# если ответ не правильный

					else:
						# находим и выводим значение неправильного ответа
						wrong_dict = ''
						if self.language == 'rus-eng':
							wrong_dict = 'eng-rus'
						if self.language == 'eng-rus':
							wrong_dict = 'rus-eng'
						base_name = 'dict/' + wrong_dict + '.all.json'
						# print(base_name)
						with open(base_name, 'r') as obj:
							diction = json.load(obj)
							for key_values in diction:
								key = key_values[0]
								values = key_values[1]
								if key == answer:
									d_w = ''
									for value in values:
										d_w += value + ', '
									print('\t' + key + ' - ' + d_w[:-2])
						# выводим правильную пару ключ-значение

						comm = ''
						for w in word[1]:
							comm += w + ', '
						print('\t' + str(word[0]) + ' - ' + comm[:-2] + '\n')
						# записываем результаты неправильного ответа
						n = int(current[2]) + 1
						del current[2]
						current.insert(2, n)
						result_test.append(current)

		# сохраняем результаты в опциях
		self.result_test = result_test

	# print('результаты теста')
	# print(result_test)

	def rewrite_result(self):
		"""вписываем новые результаты в старые"""
		with open(self.base_adress, 'r') as obj:
			old_write = json.load(obj)
		new_write = self.result_test[:]
		# заменяем новыми показателями данные в старых результатах
		keys = []
		for k in new_write:
			k_new = k[0]
			keys.append(k_new)
		for k in old_write:
			k_old = k[0]
			if k_old not in keys:
				new_write.append(k)
		self.result_test_add_old = new_write

	# print('добавляем новые в старые')
	# print(new_write)

	def recalc_indicators(self):
		"""пересчёт показателей статистики на основе новых результатов"""
		new_result = self.result_test_add_old[:]
		recalculation_dict = []
		while new_result:
			word = new_result.pop()
			yes = word[1]
			no = word[2]
			# заменяем процент правильных ответов
			if yes > 0:
				percent = int(yes * 100 / (yes + no))
			else:
				percent = 0
			del word[3]
			word.insert(3, percent)
			# заменяем количество попыток
			count = int(yes + no)
			del word[4]
			word.insert(4, count)
			# сохраняем пересчёт
			recalculation_dict.append(word)
		self.result_data = recalculation_dict

	# print('обновляем показатели')
	# print(recalculation_dict)

	def json_dump(self):
		"""записываем в файл"""
		with open(self.base_adress, 'w') as obj:
			json.dump(self.result_data, obj)
