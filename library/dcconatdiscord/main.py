import requests, pymysql, json, os, re

class DCConAtDiscord:
	def getJSONStyle(self, text: str):
		return text.replace('	', '').replace(' ', '').replace('\n', '').replace('},{', '},\n{')
	
	def getFileFromURL(self, url: str, path: str):
		fileRaw = requests.get(url, allow_redirects=True)

		pathFolder = '/'.join(path.split('/')[:-1])+'/'

		if(not os.path.exists(pathFolder)):
			os.mkdir(pathFolder)

		if(not os.path.exists(path)):
			open(path, 'wb').write(fileRaw.content)

		return 0