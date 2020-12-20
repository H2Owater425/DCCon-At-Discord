import requests, pymysql, shutil, json, os, re
from dotenv import load_dotenv

load_dotenv(verbose=True)

DATABASE = json.loads(os.getenv('DATABASE').replace('\'', '"'))
database = pymysql.connect(host=DATABASE['host'], port=DATABASE['port'], user=DATABASE['user'], password=DATABASE['password'], database=DATABASE['database'], charset='utf8')
cursor = database.cursor()

def getJSONStyle(text):
	return text.replace('	', '').replace(' ', '').replace('\n', '').replace('},{', '},\n{')

def getFileFromURL(URL):
	fileName = URL.split('/')[len(URL.split('/'))-1]
	fileRaw = requests.get(URL, allow_redirects=True)
	open(f'./images/{fileName}', 'wb').write(fileRaw.content)

funzinnuFDF = '['+getJSONStyle(requests.get('https://www.funzinnu.com/stream/dccon.js').text[15:-3])+']'

telkODF = '['+getJSONStyle(requests.get('http://tv.telk.kr/json').text.replace(',"path":"', ',"path":"http://tv.telk.kr/images/'))[11:-2]+']'

yeokkaODF = '['+getJSONStyle(requests.get('https://watert.gitlab.io/emotes/yeokka/ODF.json').text)[11:-2]+']'

poopkiODF = getJSONStyle(requests.get('https://raw.githubusercontent.com/poopki2018/poopki_dccon/master/chatassistx-master/dccon_ODF.json').text[13:-2])

funzinnuFDFJSON = json.loads(funzinnuFDF)

telkODFJSON = json.loads(telkODF)

yeokkaODFJSON = json.loads(yeokkaODF)

poopkiODFJSON = json.loads(poopkiODF)

i = 0
while True:
	if(i == len(funzinnuFDFJSON)):
		break
	if('파누' in funzinnuFDFJSON[i]['tags'] or '미지정' in funzinnuFDFJSON[i]['tags']):
		del funzinnuFDFJSON[i]
		i = 0
	else:
		i += 1

i = 0
while True:
	if(i == len(telkODFJSON)):
		break
	if('텔크' in telkODFJSON[i]['tags']):
		del telkODFJSON[i]
		i = 0
	else:
		j = 0
		while True:
			if(j == len(telkODFJSON[i]['keywords'])):
				break
			if(re.fullmatch(re.compile('(((.*텔.*)|(.*텔크.*))(?<!텔)$)'), telkODFJSON[i]['keywords'][j]) != None):
				del telkODFJSON[i]['keywords'][j]
				j = 0
			else:
				j += 1
		if(len(telkODFJSON[i]['keywords']) < 1):
			del telkODFJSON[i]
			i = 0
		else:
			if(len(telkODFJSON[i]['tags']) < 1):
				del telkODFJSON[i]
				i = 0
			else:
				i += 1

i = 0
while True:
	if(i == len(yeokkaODFJSON)):
		break
	if('여까티콘' in yeokkaODFJSON[i]['tags'] or '움짤' in yeokkaODFJSON[i]['tags']):
		del yeokkaODFJSON[i]
		i = 0
	else:
		if(len(yeokkaODFJSON[i]['tags']) < 1):
			del yeokkaODFJSON[i]
			i = 0
		else:
			i += 1

i = 0
while True:
	if(i == len(poopkiODFJSON)):
		break
	if('움짤' in poopkiODFJSON[i]['tags']):
		del poopkiODFJSON[i]
		i = 0
	else:
		if(len(poopkiODFJSON[i]['tags']) < 1):
			del poopkiODFJSON[i]
			i = 0
		else:
			i += 1

if(not os.path.exists('./data/funzinnuFDF.json')):
	funzinnuFDFFile = open('./data/funzinnuFDF.json', 'a', encoding='utf-8')
	funzinnuFDFFile.write(getJSONStyle(str(funzinnuFDFJSON)).replace('\'', '"'))
else:
	os.remove('./data/funzinnuFDF.json')
	funzinnuFDFFile = open('./data/funzinnuFDF.json', 'a', encoding='utf-8')
	funzinnuFDFFile.write(getJSONStyle(str(funzinnuFDFJSON)).replace('\'', '"'))

if(not os.path.exists('./data/telkODF.json')):
	telkODFFile = open('./data/telkODF.json', 'a', encoding='utf-8')
	telkODFFile.write(getJSONStyle(str(telkODFJSON)).replace('\'', '"'))
else:
	os.remove('./data/telkODF.json')
	telkODFFile = open('./data/telkODF.json', 'a', encoding='utf-8')
	telkODFFile.write(getJSONStyle(str(telkODFJSON)).replace('\'', '"'))

if(not os.path.exists('./data/yeokkaODF.json')):
	yeokkaODFFile = open('./data/yeokkaODF.json', 'a', encoding='utf-8')
	yeokkaODFFile.write(getJSONStyle(str(yeokkaODFJSON)).replace('\'', '"'))
else:
	os.remove('./data/yeokkaODF.json')
	yeokkaODFFile = open('./data/yeokkaODF.json', 'a', encoding='utf-8')
	yeokkaODFFile.write(getJSONStyle(str(yeokkaODFJSON)).replace('\'', '"'))

if(not os.path.exists('./data/poopkiODF.json')):
	poopkiODFFile = open('./data/poopkiODF.json', 'a', encoding='utf-8')
	poopkiODFFile.write(getJSONStyle(str(poopkiODFJSON)).replace('\'', '"'))
else:
	os.remove('./data/poopkiODF.json')
	poopkiODFFile = open('./data/poopkiODF.json', 'a', encoding='utf-8')
	poopkiODFFile.write(getJSONStyle(str(poopkiODFJSON)).replace('\'', '"'))

# poopkiODF > yeokkaODF > funzinnuFDF > telkODF

for i in range(len(poopkiODFJSON)):
	for j in range(len(poopkiODFJSON[i]['keywords'])):
		cursor.execute(f'INSERT IGNORE INTO `dccon` (`id`, `tag`, `url`) values (\'{poopkiODFJSON[i]["keywords"][j]}\', \'{poopkiODFJSON[i]["tags"][0]}\', \'{poopkiODFJSON[i]["path"]}\')')

for i in range(len(yeokkaODFJSON)):
	for j in range(len(yeokkaODFJSON[i]['keywords'])):
		cursor.execute(f'INSERT IGNORE INTO `dccon` (`id`, `tag`, `url`) values (\'{yeokkaODFJSON[i]["keywords"][j]}\', \'{yeokkaODFJSON[i]["tags"][0]}\', \'{yeokkaODFJSON[i]["path"]}\')')

for i in range(len(funzinnuFDFJSON)):
	for j in range(len(funzinnuFDFJSON[i]['keywords'])):
		cursor.execute(f'INSERT IGNORE INTO `dccon` (`id`, `tag`, `url`) values (\'{funzinnuFDFJSON[i]["keywords"][j]}\', \'{funzinnuFDFJSON[i]["tags"][0]}\', \'{funzinnuFDFJSON[i]["uri"]}\')')

for i in range(len(telkODFJSON)):
	for j in range(len(telkODFJSON[i]['keywords'])):
		cursor.execute(f'INSERT IGNORE INTO `dccon` (`id`, `tag`, `url`) values (\'{telkODFJSON[i]["keywords"][j]}\', \'{telkODFJSON[i]["tags"][0]}\', \'{telkODFJSON[i]["path"]}\')')

database.commit()

database.close()