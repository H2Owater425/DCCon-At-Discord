import requests, pymysql, shutil, json, os, re
from dotenv import load_dotenv

load_dotenv(verbose=True)

DATABASE = json.loads(os.getenv('DATABASE').replace('\'', '"'))
database = pymysql.connect(host=DATABASE['host'], port=DATABASE['port'], user=DATABASE['user'], password=DATABASE['password'], database=DATABASE['database'], charset='utf8')
cursor = database.cursor()

def getJSONStyle(text):
	return text.replace('	', '').replace(' ', '').replace('\n', '').replace('},{', '},\n{')

def getFixedTag(keyword, tag):
	originList = ['RCT', '롤코타', '계란', '달걀콘', '눈물콘', '냥이', '동숲', '레바콘', '마울어', '마크', '문풍당당', '이풍당당', '예풍당당', '볼트보이콘', '북돼지', '이북리더', '심의콘', '시스카', '젤다', '짜잔콘', '샌즈', '캐피탈리즘호', '카티아', '컴', '컴갤콘', '토드콘', '포켓몬']
	fixedList = ['롤러코스터타이쿤', '롤러코스터타이쿤', '껍질미리깐달걀', '껍질미리깐달걀', '눈물', '고양이', '동물의숲', '레바', '마이너울트라어드벤처', '마인크래프트', '당당', '당당', '당당', '볼트보이', '김정은', '김정은', '심의', '시티즈스카이라인', '젤다의전설', '제프카플란', '언더테일', '루세티아', '카티아마나간', '컴퓨터', '컴퓨터갤러리', '토드하워드', '포켓몬스터']

	if(keyword == '태극기' and tag == '국뽕'):
		tag = '국기'
	elif(keyword == '펄럭2' and tag == '깃발'):
		tag = '국뽕'
	elif(keyword == '유다희5' and tag == '다크소울'):
		tag = '유다이'
	elif(keyword == '받아치기1' and tag == '애니' or keyword == '안녕하살법1' and tag == '애니'):
		tag = '카구야님은고백받고싶어'
	elif(keyword == '변태이용가' and tag == '히토미'):
		tag = '심의'
	else:
		if(tag in originList):
			tag = fixedList[originList.index(tag)]
	return tag

#def getFileFromURL(URL):
#	fileName = URL.split('/')[len(URL.split('/'))-1]
#	fileRaw = requests.get(URL, allow_redirects=True)
#	open(f'./images/{fileName}', 'wb').write(fileRaw.content)

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
		poopkiODFJSON[i]['tags'][0] = getFixedTag(poopkiODFJSON[i]["keywords"][j], poopkiODFJSON[i]['tags'][0])
		cursor.execute(f'INSERT IGNORE INTO `dccon` (`id`, `tag`, `url`, `last_update`) values (\'{poopkiODFJSON[i]["keywords"][j]}\', \'{poopkiODFJSON[i]["tags"][0]}\', \'{poopkiODFJSON[i]["path"]}\', CURDATE())')

for i in range(len(yeokkaODFJSON)):
	for j in range(len(yeokkaODFJSON[i]['keywords'])):
		yeokkaODFJSON[i]['tags'][0] = getFixedTag(yeokkaODFJSON[i]["keywords"][j], yeokkaODFJSON[i]['tags'][0])
		cursor.execute(f'INSERT IGNORE INTO `dccon` (`id`, `tag`, `url`, `last_update`) values (\'{yeokkaODFJSON[i]["keywords"][j]}\', \'{yeokkaODFJSON[i]["tags"][0]}\', \'{yeokkaODFJSON[i]["path"]}\', CURDATE())')

for i in range(len(funzinnuFDFJSON)):
	for j in range(len(funzinnuFDFJSON[i]['keywords'])):
		funzinnuFDFJSON[i]['tags'][0] = getFixedTag(funzinnuFDFJSON[i]["keywords"][j], funzinnuFDFJSON[i]['tags'][0])
		cursor.execute(f'INSERT IGNORE INTO `dccon` (`id`, `tag`, `url`, `last_update`) values (\'{funzinnuFDFJSON[i]["keywords"][j]}\', \'{funzinnuFDFJSON[i]["tags"][0]}\', \'{funzinnuFDFJSON[i]["uri"]}\', CURDATE())')

for i in range(len(telkODFJSON)):
	for j in range(len(telkODFJSON[i]['keywords'])):
		telkODFJSON[i]['tags'][0] = getFixedTag(telkODFJSON[i]["keywords"][j], telkODFJSON[i]['tags'][0])
		cursor.execute(f'INSERT IGNORE INTO `dccon` (`id`, `tag`, `url`, `last_update`) values (\'{telkODFJSON[i]["keywords"][j]}\', \'{telkODFJSON[i]["tags"][0]}\', \'{telkODFJSON[i]["path"]}\', CURDATE())')

database.commit()

database.close()