# проверка на дубли слов в базе

import json

with open('я.rus-eng.result.json', 'r') as obj:
	old_data = json.load(obj)
	new_data = []

	recalculation_dict = []
	while old_data:
		word = old_data.pop()
		yes = word[1] -1
		del word[1]
		word.insert(1, yes)
		no = word[2] - 1
		del word[2]
		word.insert(2, no)
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
		new_data.append(word)

with open('я.rus-eng.new_result.json', 'w') as obj:
	json.dump(new_data, obj)