import pymysql, json, os, requests
from dotenv import load_dotenv

load_dotenv(verbose=True)

DATABASE = json.loads(os.getenv('DATABASE').replace('\'', '"'))

def getFileFromURL(url, path):
	fileRaw = requests.get(url, allow_redirects=True)
	pathFolder = '/'.join(path.split('/')[:-1])+'/'
	if(not os.path.exists(pathFolder)):
		os.mkdir(pathFolder)
	if(not os.path.exists(path)):
		open(path, 'wb').write(fileRaw.content)
	print(path)

database = pymysql.connect(host=DATABASE['host'], port=DATABASE['port'], user=DATABASE['user'], password=DATABASE['password'], database=DATABASE['database'], charset='utf8', cursorclass=pymysql.cursors.DictCursor)
cursor = database.cursor()
cursor.execute(f'SELECT * FROM `dccon`')
searchResult = cursor.fetchall()

for i in range(len(searchResult)):
	if(not os.path.exists(f'./images/{searchResult[i]["tag"]}/{searchResult[i]["id"]}.'+searchResult[i]['url'].split('/')[-1:][0].split('.')[-1:][0])):
		getFileFromURL(searchResult[i]['url'], f'./images/{searchResult[i]["tag"]}/{searchResult[i]["id"]}.'+searchResult[i]['url'].split('/')[-1:][0].split('.')[-1:][0])