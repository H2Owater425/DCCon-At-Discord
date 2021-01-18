import requests, os
from bs4 import BeautifulSoup

def getDCConData(packageName: str):
	try:
		DCCON_HOME_URL = 'https://dccon.dcinside.com/'
		DCCON_SEARCH_URL = 'https://dccon.dcinside.com/hot/1/title/'
		DCCON_DETAILS_URL = 'https://dccon.dcinside.com/index/package_detail'

		session = requests.Session()

		packageSearchRaw = session.get(DCCON_SEARCH_URL+packageName)
		packageSearchHtml = BeautifulSoup(packageSearchRaw.text, 'html.parser')
		packageSearchList = packageSearchHtml.select('#right_cont_wrap > div > div.dccon_listbox > ul > li')

		if(len(packageSearchList) != 0):
			targetPackage = packageSearchList[0]
			targetPackageNumber = targetPackage.get('package_idx')
			targetPackageName = targetPackage.select_one('a > strong.dcon_name').text

			if(targetPackageNumber == '15276' and not packageName in ['두', '두콘', '료', '만', '만두', '만두콘', '만두콘 무료', '무', '무료', '콘']):
				raise Exception(f'no dccon package name: {packageName}')

			print(targetPackageName, targetPackageNumber)
		
		else:
			raise Exception(f'no dccon package name: {packageName}')

	except Exception as error:
		print(error)

while True:
	try:
		getDCConData(input())
	
	except:
		break