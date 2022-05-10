# -----NEW
# НОВЫЕ СЛОВА изначальный показатель 50/50% (правильные/неправильные) 
# слово, значение которого пользователь ранее не вводил
# / добавляютя при при наличии старых результатах до 20 слов с показателем менее 50%

# -----LO%
# ПЛОХИЕ РЕЗУЛЬТАТЫ
# слово с самым низким показателем качества ответов (правильные/неправильные) 
# / добавляется всегда

# -----BEG
# НОВИЧОК мало изученное, не набравшее статистики
# слово, которое показывалось менее 5-ти раз
# / добавляется всегда

# -----OLD
# РАНДОМНЫЕ СТАРЫЕ
# слово которые уже показывались ранее
# / добавляютя при при наличии старых результатах до 20 слов с показателем менее 50%

# -----L/B
# чтото среднее между LO% и BEG
# слово, самые низкие показатели правильных_ответов/количеству показов на индекс ответов до [8]
# / добавляютя при при наличии старых результатах до 20 слов с показателем менее 50%

# -----------------
# возможно в функции arrangement стоит добавить условия запуска вложенных функций


import random
import json
from operator import itemgetter

# from math import ceil


class CreateTest():
	"""создание словаря для тестов"""

	def __init__(self, base_adress, language_type):
		self.base_adress = base_adress
		self.language_type = language_type
		self.p_l = 'none'
		# словарь с словами для теста
		self.test_dictionary = []

	def arrangement(self):
		"""создание и заполнение теста"""
		# проверка количества слов с низким качеством ответов
		# print(self.rate_percent(61))
		if self.rate_percent(61) > 24:
			# print(self.rate_percent(61))
			# добавляем мало изученные слова
			self.dict_word_low_percent()
		else:
			# добавляем новые слова
			self.dict_word_new()
			if self.idex_min_percent(24, 71):
				self.dict_word_new()
			if self.idex_min_percent(26, 81):
				self.dict_word_new()
			# добавляем малоизученные слова BEGINER
			self.world_small_views()
			# добавляем известные слова
			for test in range(1, int(self.len_old_result()/500+1)):
				self.dict_word_old_random()
			# добавляем слово, самые низкие показатели правильных_ответов/количеству показов
			self.black_sheep()
			# добавляем мало изученные слова
			self.dict_word_low_percent()

		# print(self.test_dictionary)
		return self.test_dictionary

	def base_check(self):
		"""проверка ответов на наличие отсутствующих в базе слов, и их удаление"""
		# добываем все ключи из словаря
		all_keys = []
		data_all_words = self.extract_dict_values_all()
		if data_all_words:
			for word_for_key in data_all_words:
				key = word_for_key[0]
				all_keys.append(key)
		# провер очка базы предыдущих ответов
		data_old_result = self.extract_dict_result()
		if data_old_result:
			bad_words = []
			good_words = []
			for old_result_word in data_old_result:
				key = old_result_word[0]
				if key in all_keys:
					good_words.append(old_result_word)
				if key not in all_keys:
					bad_words.append(old_result_word)
			# записываем словарь обратно
			with open(self.base_adress, 'w') as obj:
				json.dump(good_words, obj)
			# информируем пользователя об удалении слов из базы ответов
			if bad_words:
				print("ВНИМАНИЕ из базы удалены устаревшие слова:")
				for word in bad_words:
					key = word[0]
					print('\t' + key)
				print()

	def dict_word_new(self):
		'''подбор слов новых'''
		data_words_new = self.word_new()
		if data_words_new:
			# проверка хреновых показателей ;)
			# self.rate_percent(61)
			# узнаем количество малоизученных
			# при условии добавляем новое слово в тест
			a = self.idex_min_percent(22, 61)
			if a:
				b = self.idex_min_percent(20, 51)
				if a and b:
					index = random.randint(0, len(data_words_new) - 1)
					new_word = data_words_new[index]
					if new_word not in self.test_dictionary:
						self.test_dictionary.append(new_word)
						# print('-----NEW')
						# print(new_word)
			# первый запуск
			data_old_result = self.extract_dict_result()
			if (data_old_result == None) or len(data_old_result) < 10:
				index = random.randint(0, len(data_words_new) - 1)
				new_word = data_words_new[index]
				if new_word not in self.test_dictionary:
					self.test_dictionary.append(new_word)
					# print('-----NEW')
					# print(new_word)

	def rate_percent(self, percent):
		"""показать количество слов, ниже определённого показателя % правильных ответов"""
		data_old_result = self.extract_dict_result()
		if data_old_result:
			low_percent = []
			for word in data_old_result:
				if word[3] < percent:
					low_percent.append(word)
			if low_percent:
				return (len(low_percent))
		return 0

	def black_sheep(self):
		'''слово, самые низкие показатели правильных_ответов/количеству показов'''
		data_old_result = self.extract_dict_result()
		if data_old_result and len(data_old_result) > 5:
			rate = len(data_old_result) / 50
			# собираем варианты количества ответов
			variant_indices = []
			for word in data_old_result:
				index = word[4]
				if (index < int(rate)) and (index not in variant_indices):
					variant_indices.append(index)
			# создаем словарь, где для каждого индекса свой список
			break_for_indices = {}
			for index in variant_indices:
				break_for_indices[index] = []
			# добавляем слова в словарь по индексам
			for word in data_old_result:
				index_word = word[4]
				for i, diction in break_for_indices.items():
					if i == index_word:
						dict_for_append = diction
						dict_for_append.append(word)
						break_for_indices[i] = dict_for_append
			# создаём список самых слов
			bad = []
			for key, value in break_for_indices.items():
				sort_value = sorted(value, key=itemgetter(int(3)))
				word = sort_value.pop(0)
				bad.append(word)
			if bad:
				index_add = random.randint(0, len(bad) - 1)
				new_word = bad[index_add]
				if new_word not in self.test_dictionary:
					self.test_dictionary.append(new_word)

	# print('-----L/B')
	# print(bad)

	def world_small_views(self):
		'''новичок'''
		new_word = self.index_min_view_percent(4, 100)
		if new_word:
			if new_word not in self.test_dictionary:
				self.test_dictionary.append(new_word)
		# print('-----BEG')
		# print(new_word)

	def dict_word_old_random(self):
		'''подбор слов старых(временная функция - для теста)'''
		data_rate = self.idex_min_percent(20, 51)
		if data_rate:
			data_old_result = self.extract_dict_result()
			if data_old_result:
				index = random.randint(0, len(data_old_result) - 1)
				new_word = data_old_result[index]
				if new_word not in self.test_dictionary:
					self.test_dictionary.append(new_word)
			# print('-----OLD')
			# print(new_word)

	def dict_word_low_percent(self):
		'''подбор слов с низким %'''
		data_old_result = self.extract_dict_result()
		if data_old_result:
			dict_sort = sorted(data_old_result, key=itemgetter(int(3)))
			new_word = dict_sort.pop(0)
			#print(new_word)
			if new_word not in self.test_dictionary:
				self.test_dictionary.append(new_word)
		# print('-----LO%')
		# print(new_word)

	def word_new(self):
		'''извлечение всех новых слов из текущего словаря'''

		# открываем предыдущие результаты
		data_old_result = self.extract_dict_result()
		if data_old_result:
			#
			len_old_result = len(data_old_result) + 10
			active = True
			num_dict = 1
			while active:
				num_file_name = 'dict/' + self.language_type + '.' + str(num_dict) + '.json'
				with open(num_file_name, 'r') as obj:
					read_dict = obj.read()
					upload_dict = eval(read_dict)
					dict_len = len(upload_dict)
				# пробуем по очереди словари сравнивая количество
				# протестированных слов c объемом словаря
				if len_old_result < dict_len:
					# print('слов изучено ' + str(len_old_result))
					# print('слов для теста ' + str(dict_len))
					self.p_l = str(num_dict)
					active = False
				num_dict += 1

			# открываем подходящий словарь
			data_dictionary_words = self.extract_dict_value()
			if data_dictionary_words:
				# создаем список новых слов
				new_words = []
				key_old_result = []
				# собираем ключи предыдущих результатов
				for old_key in data_old_result:
					key_old_result.append(old_key[0])
				# добавляем ранее не использованные слова
				for new_word in data_dictionary_words:
					new_key = new_word[0]
					if new_key not in key_old_result:
						example = [new_key, 0, 0, 0, 0]
						new_words.append(example)
						# print(new_words)
						return new_words[:]
		# при первом запуске
		else:
			self.p_l = 1
			# открываем подходящий словарь
			data_dictionary_words = self.extract_dict_value()
			if data_dictionary_words:
				# создаем список новых слов
				new_words = []
				key_old_result = []
				for new_word in data_dictionary_words:
					new_key = new_word[0]
					example = [new_key, 0, 0, 0, 0]
					new_words.append(example)
					# print(new_words)
					return new_words[:]

	def extract_dict_value(self):
		'''распаковка словаря с значениями'''
		dict_name = 'dict/' + self.language_type + '.' + str(self.p_l) + '.json'
		with open(dict_name, 'r') as obj:
			data = json.load(obj)
			if data:
				return data[:]

	def extract_dict_values_all(self):
		'''распаковка словаря с значениями_all'''
		dict_name = 'dict/' + self.language_type + '.all.json'
		with open(dict_name, 'r') as obj:
			data = json.load(obj)
			if data:
				return data[:]

	def idex_min_percent(self, max_amount, percent):
		'''допуск, макс кол-ва слов с определённым показателем % правильных ответов'''
		data_old_result = self.extract_dict_result()
		if data_old_result:
			low_percent = []
			for word in data_old_result:
				if word[3] < percent:
					low_percent.append(word)
			# print(len(low_percent))
			if len(low_percent) < max_amount:
				return True
			else:
				return False

	def index_min_view_percent(self, view, percent):
		'''подбор слов со значениями показов и правильных ответов'''
		'''меньше заданных показателей'''
		data_old_result = self.extract_dict_result()
		if data_old_result:
			words = []
			for word in data_old_result:
				p = word[3]
				v = word[4]
				if int(v) < view and int(p) < percent:
					words.append(word)
			if words:
				index = random.randint(0, len(words) - 1)
				new_word = words[index]
				return new_word

	def extract_dict_result(self):
		'''распакока словаря предыдущих результатов'''
		with open(self.base_adress, 'r') as obj:
			data = json.load(obj)
			# print(self.base_adress)
			# print(data)
			if data:
				return data[:]

	def len_old_result(self):
		"""количество слов протестированных"""
		data = self.extract_dict_result()
		if data:
			len_data = len(data)
		else:
			len_data = 0
		return len_data