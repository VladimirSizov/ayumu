# проверка на дубли слов в базе

import json

bad_word = 'бедные,. плохой'

with open('я.rus-eng.result.json', 'r') as obj:
	old_data = json.load(obj)
	new_data = []
	for base_word in old_data:
		key = base_word[0]
		if key == bad_word:
			print('слово "' + bad_word + '" найдено и удалено.')
		else:
			new_data.append(base_word)

with open('я.rus-eng.new_result.json', 'w') as obj:
	json.dump(new_data, obj)
