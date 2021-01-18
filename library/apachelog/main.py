import re, os
from datetime import datetime
from pytz import timezone

class ApacheLog:
	
	def __init__(self, export: str=None):
		self.export = export

	def log(self, timeZone: str, logLevel: str or int, message: str, export: str=None) -> None:
		'''
		Print or saves apache-formed log

		- logLevel: debug=0 | info=1 | notice=2 | warn=3 | alert=4 | error=5 | crit=6 | emerg=7
		- export: _PathLike
		'''

		if(str(type(timeZone)) != '<class \'str\'>'):
			raise TypeError('unsupported type for timeZone('+str(type(logLevel)).replace('<class \'', '').replace('\'>', '')+')')

		elif(str(type(logLevel)) != '<class \'str\'>' and str(type(logLevel)) != '<class \'int\'>'):
			raise TypeError('unsupported type for logLevel('+str(type(logLevel)).replace('<class \'', '').replace('\'>', '')+')')

		elif(str(type(message)) != '<class \'str\'>'):
			raise TypeError('unsupported type for message('+str(type(logLevel)).replace('<class \'', '').replace('\'>', '')+')')

		elif(str(type(export)) != '<class \'str\'>' and str(type(export)) != '<class \'NoneType\'>'):
			raise TypeError('unsupported type for export('+str(type(logLevel)).replace('<class \'', '').replace('\'>', '')+')')

		# debug: 0, info: 1, notice: 2, warn: 3, alert: 4, error: 5, crit: 6, emerg: 7
		logLevelNameList = ['debug', 'info', 'notice', 'warn', 'alert', 'error', 'crit', 'emerg']

		if(export == None):
			export = self.export

		else:
			export = export.replace('\\', '/')

		if(re.match(re.compile('^[+-](?:2[0-3]|[01][0-9]):[0-5][0-9]$'), timeZone) == None):
			raise ValueError(f'unsupported string form for timeZone("{timeZone}")')

		if(str(type(logLevel)) == '<class \'str\'>'):
			if(not logLevel in logLevelNameList):
				raise ValueError(f'unsupported string form for logLevel("{logLevel}")')

		elif(str(type(logLevel)) == '<class \'int\'>'):
			if(logLevel < 8 and logLevel > -1):
				logLevel = logLevelNameList[logLevel]

			else:
				raise ValueError(f'unsupported integer for logLevel("{logLevel}")')

		if(export != None):
			if(len(export.split('/')[:-1]) != 0 and not os.path.exists('/'.join(export.split('/')[:-1]))):
				os.mkdir('/'.join(export.split('/')[:-1]))

			try:
				logFile = open(export, 'a', encoding='utf8')

			except PermissionError:
				raise PermissionError(f'wrong or have no permission for log file("{export}")')

			currentTime = datetime.now(timezone("UTC")).strftime('%d/%b/%Y:%H:%M:%S')

			print(f'[{currentTime} {timeZone}][{logLevel}] {message}')

			logFile.write(f'[{currentTime} {timeZone}][{logLevel}] {message}\n')
			logFile.close()

		else:
			currentTime = datetime.now(timezone("UTC")).strftime('%d/%b/%Y:%H:%M:%S')

			print(f'[{currentTime} {timeZone}][{logLevel}] {message}')

		return None

def log(timeZone: str, logLevel: str or int, message: str, export: str=None) -> None:
	'''
	Print or saves apache-formed log

	- logLevel: debug=0 | info=1 | notice=2 | warn=3 | alert=4 | error=5 | crit=6 | emerg=7
	- export: _PathLike
	'''
	
	log = ApacheLog().log

	log(timeZone, logLevel, message, export)