import json

# переделываем словари слов из состояния: [word, answers "ye", answers "no"]
# в [word, answers "ye", answers "no", percent "yes" from all, count try]
filename = 'я.er.json'
with open(filename, 'r') as obj:
	read_dict = obj.read()
	upload_dict = eval(read_dict)
	
	new = []
	while upload_dict:
		word = upload_dict.pop()
		yes = int(word[1])
		no = int(word[2])
		# заменяем строчные значения на числовые
		del word[1]
		word.insert(1, yes)
		del word[2]
		word.insert(2, no)
		# добавляем процент правильных ответов
		if yes > 0:
			percent = int(yes * 100 / (yes + no))
		else:
			percent = 0
		word.append(percent)
		count = int(yes + no)
		word.append(count)
		new.append(word)

# перезаписываем результат 
new_filename = 'я.eng-rus.result.json'
with open(new_filename, 'w') as obj:
	json.dump(new, obj)
		
