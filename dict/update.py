import json

# собираем все слова в один словарь eng-rus
all_words = ['1-1000', '1001-2000', '2001-3000', '3001-4000', '4001-5000']

update_eng_rus = []
for thousand in all_words:
	name_thousand = thousand + '.json'
	with open(name_thousand, 'r', encoding='utf-8') as f_obj:
		read_dict = f_obj.read()
		read_dict = read_dict.rstrip()
		dict_update = eval(read_dict)
		while dict_update:
			cut = dict_update.pop(0)
			update_eng_rus.append(cut)



# создаем словари eng-rus
max_num_dict = int(len(update_eng_rus)/100)+1

for list_amount in range(1, max_num_dict):
	end_num_word = list_amount * 100
	dictionary = update_eng_rus[:end_num_word]
	eng_rus_name = 'eng-rus.' + str(list_amount)+ '.json'
	print(str(list_amount) + 'eng-rus' + str(len(dictionary)))
	with open(eng_rus_name, 'w') as obj:
		json.dump(dictionary, obj)

# создаём полный словарь eng-rus
all_eng_rus_name = 'eng-rus.all.json'
with open(all_eng_rus_name, 'w') as obj:
	json.dump(update_eng_rus, obj)

# создаем словарь rus-eng
eng_rus_name = 'eng-rus.' + str(max_num_dict - 1) + '.json'
with open(eng_rus_name, 'r') as obj:
	read_dict = obj.read()
	upload_dict = eval(read_dict)

	dictionary = []
	# потрошим словарь eng-rus
		
	# получаем русские ключи
	rus_eng_keys = []
	for key_values in upload_dict:
		values = key_values[1]
		for value in values:
			if value not in rus_eng_keys:
				rus_eng_keys.append(value)
		#
	for rus_key in rus_eng_keys:
		rus_word = []
		rus_word.append(rus_key)
		# добываем английские значения
		rus_values = []
		for key_values in upload_dict:
			key = key_values[0]
			values = key_values[1]
			for value in values:
				if value == rus_key:
					if key not in rus_values:
						rus_values.append(key)
		rus_word.append(rus_values)
			# мы создали пары ключ-значение, записываем в словарь для экспорта
		dictionary.append(rus_word)
	#print(dictionary)
	print(str(len(dictionary)))

# создаём полный словарь rus-eng
all_rus_eng_name = 'rus-eng.all.json'
with open(all_rus_eng_name, 'w') as obj:
	json.dump(dictionary, obj)

# создаем списки rus_eng
for list_amount in range(1, max_num_dict):

	# извлекаем все ключи из текущего словаря eng-rus
	eng_rus_name = 'eng-rus.' + str(list_amount)+ '.json'
	with open(eng_rus_name, 'r') as obj:
		read_dict = obj.read()
		upload_dict = eval(read_dict)

	# потрошим словарь eng_rus и получаем русские ключи
	rus_eng_keys = []
	for key_values in upload_dict:
		values = key_values[1]
		for value in values:
			if value not in rus_eng_keys:
				rus_eng_keys.append(value)

	# создаем словарь rus-eng добавляем значения по руским ключам
	rus_eng_dictionary = []
	for key_values in dictionary:
		key = key_values[0]
		value = key_values[1]
		if key in rus_eng_keys:
			rus_eng_dictionary.append(key_values)

	# print(rus_dictionary)
	# print(str(len(rus_eng_dictionary)))

	# создаем словарь rus_eng
	rus_eng_name = 'rus-eng.' + str(list_amount) + '.json'
	print(str(list_amount) + 'rus-eng' + str(len(rus_eng_dictionary)))
	with open(rus_eng_name, 'w') as obj:
		json.dump(rus_eng_dictionary, obj)

