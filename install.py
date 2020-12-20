import os, sys

pythonVersion = sys.version_info.major
operatingSystem = sys.platform

if(operatingSystem == 'linux' or operatingSystem == 'linux2'):
# Linux platform
	clear = 'clear'
elif(operatingSystem == 'darwin'):
# macOS platform
	clear = 'clear'
elif(operatingSystem == 'win32'):
# Windows platform
	clear = 'cls'
else:
	clear = 'clear'

if(pythonVersion == '1'):
	pip = 'pip1'
elif(pythonVersion == '2'):
	pip = 'pip2'
elif(pythonVersion == '3'):
	pip = 'pip3'

print('Install dependences...')
try:
	os.system(f'{pip} install discord asyncio pymysql python-dotenv datetime pytz')
except Exception as execption:
	print(f'Error occurred: {Exception}')

os.system(clear)
print('Finished!')