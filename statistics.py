import json
import math
from create_test import CreateTest


class Statistics():
	"""статистика"""

	def __init__(self, base_adress, percent_know):
		a = 1
		self.base_adress = base_adress
		self.percent_know = percent_know

	def previous_results(self):
		"""результаты предыдущих достижений"""
		#
		self.count_y_n(self.base_adress, self.percent_know)
		#
		self.param_answers()
		print('\nПриступим:')

	def count_y_n(self, base_adress, percent_know):
		"""подсчет выученных слов"""
		with open(base_adress, 'r') as obj:
			lexicon = json.load(obj)
		all_yes = 0
		all_no = 0
		know = []
		does_not_know = []
		if lexicon:
			for word in lexicon:
				w = word[0]
				y = int(word[1])
				all_yes += int(word[1])
				n = int(word[2])
				all_no += int(word[2])
				if y > 1 and 101 > 100 / (y + n) * y > int(percent_know):
					know.append(w)
				else:
					does_not_know.append(w)

		# подсчет  выученных слов
		level = len(lexicon)
		p_l = ''
		if int(level) < 30:
			p_l = 'A0 Basic. Starter (людоедка Эллочка)'
		if 29 < int(level) < 300:
			p_l = 'A0 Basic. Starter (людоед племени Мумбо-Юмбо)'
		if 299 < int(level) < 1500:
			p_l = 'A1 Beginner (Breakthrough or beginner)'
		if 1499 < int(level) < 2500:
			p_l = 'A2 Elementary (Way stage or elementary)'
		if 2499 < int(level) < 3250:
			p_l = 'B1 Intermediate (Threshold or intermediate)'
		if 3249 < int(level) < 3750:
			p_l = 'B2 Upper Intermediate (Vantage or upper intermediate)'
		if 3749 < int(level) < 4500:
			p_l = 'C1 Advanced (Effective operational proficiency or advanced)'
		if int(level) > 4499:
			p_l = 'C2 Fluent (Mastery or proficiency)'

		# выводим результаты
		print('Переведено при помощи GoogleTranslate')
		print('\nУровень Вашего словарного запаса: ' + p_l)
		print('Тестированных слов: ' + str(len(lexicon)))
		print('Изученых слов: ' + str(len(know)))
		print('Количество попыток: ' + str(int(all_yes + all_no)))
		if all_no or all_yes:
			print('Показатель правильных ответов: ' + str(int(all_yes * 100 / (all_yes + all_no))) + '%\n')
		print('Статистика ответов:')

	def param_answers(self):
		"""получение параметров из базы предыдущих опросов"""
		with open(self.base_adress, 'r') as obj:
			data_old_result = json.load(obj)
		if data_old_result:
			text = str(len(data_old_result)) + 'слов протестировано.'
			verified = text
			# собираем варианты количества ответов
			variant_indices = []
			for word in data_old_result:
				index = word[4]
				if index not in variant_indices:
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
			sorted(break_for_indices.items())

			for key, value in sorted(break_for_indices.items())[:20]:
				sum_result = []
				for word in value:
					word_result = word[3]
					sum_result.append(word_result)
				# считаем средний показатель качества ответа
				sum_point = 0
				len_result = len(sum_result)
				for result in sum_result:
					sum_point += result

				average = int(sum_point) / int(len_result)
				info = 'попыток: ' + str(key) + ', слов: ' + str(len_result) + ', правильно: ' + str(int(average)) + '%'
				print(info)

			return verified
