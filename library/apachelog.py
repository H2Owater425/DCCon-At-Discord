import re
from datetime import datetime
from pytz import timezone

def log(timeZone:str, logLevel:int, message:str):
	
	timeZonePattern = re.compile('^[+-](?:2[0-3]|[01][0-9]):[0-5][0-9]$')
	if(re.match(timeZonePattern, timeZone) == None):
		raise Exception(f'PatternError: unsupported string \'{timeZone}\' for timeZone')

	if(logLevel > 4 or logLevel < -4):
		raise Exception(f'RangeError: unsupported integer \'{logLevel}\' for logLevel')

	logNameList = ['emerg', 'crit', 'error', 'alert', 'warn', 'notice', 'info', 'debug']

	currentTime = datetime.now(timezone("UTC")).strftime('%d/%b/%Y:%H:%M:%S')

	return print(f'[{currentTime} {timeZone}][{logNameList[logLevel+4]}] {message}')