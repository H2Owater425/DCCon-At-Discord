import discord, asyncio, pymysql, os, json
from library.apachelog import log
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(verbose=True)

TOKEN = os.getenv('TOKEN')
PREFIX = os.getenv('PREFIX')
SUB_PREFIX = os.getenv('SUB_PREFIX')
DATABASE = json.loads(os.getenv('DATABASE').replace('\'', '"'))
PEPRE_COLOR = 0x5c7fd1
BOT_COMMAND = {
	'system': {
		'help': {
			'name': '도움말', 'description': f'`{PREFIX}도움말`', 'command': f'{PREFIX}도움말'
		}
	},
	'dccon': {
		'registered_dccon': {
			'name': '등록된 디씨콘', 'description': f'`{SUB_PREFIX}<별칭>`', 'command': None
		},
		'unregistered_dccon': {
			'name': '미등록된 디씨콘', 'description': f'`{SUB_PREFIX}<패키지> <번호|이름>`', 'command': None
		}
	}
}

def getLocation(context):
	return f'{context.guild.name} > {context.channel.name} > {context.author.name}'

app = commands.Bot(command_prefix=PREFIX)

pymysql.connect(host=DATABASE['host'], port=DATABASE['port'], user=DATABASE['user'], password=DATABASE['password'], database=DATABASE['database'], charset='utf8')
log('+09:00', 2, f'Logged in database as {DATABASE["user"]} @ {DATABASE["host"]}')

@app.event 
async def on_ready():
	await app.change_presence(status=discord.Status.online, activity=discord.Game(BOT_COMMAND['system']['help']['command']))
	log('+09:00', 2, f'Logged in discord as {app.user.name}({app.user.id}) @ DISCORD')

@app.event
async def on_message(context):
	command, argument = context.content.split(' ')[0], context.content.split(' ')[1:]

	if(command.startswith(PREFIX) and not context.author.bot):
		# ~!command arguments

		if(command == BOT_COMMAND['system']['help']['command']):
			# ~!도움말
			log('+09:00', 2, f'"{command}" @ "'+getLocation(context)+'"')
			response = discord.Embed(title='DCCon@Discord | Commands', color=PEPRE_COLOR)
			response.add_field(name=BOT_COMMAND['dccon']['registered_dccon']['name'], value=BOT_COMMAND['dccon']['registered_dccon']['description'])
			response.add_field(name=BOT_COMMAND['dccon']['unregistered_dccon']['name'], value=BOT_COMMAND['dccon']['unregistered_dccon']['description'])
			response.add_field(name='\u200b', value=f'\u200b')
			response.add_field(name=BOT_COMMAND['system']['help']['name'], value=BOT_COMMAND['system']['help']['description'])
			await context.channel.send(embed=response)
		else:
			log('+09:00', 0, f'"{command}" is not a command @ "'+getLocation(context)+'"')

	elif(command.startswith(SUB_PREFIX) and not context.author.bot):
		# ~콘이름 | ~패키지 콘이름

		if(len(argument) > 0):
			# ~패키지 콘이름
			pass
		else:
			# ~콘이름
			log('+09:00', 2, f'"{command}" @ "'+getLocation(context)+'"')
			dcConName = pymysql.escape_string(command.replace(SUB_PREFIX, ''))
			database = pymysql.connect(host=DATABASE['host'], port=DATABASE['port'], user=DATABASE['user'], password=DATABASE['password'], database=DATABASE['database'], charset='utf8')
			cursor = database.cursor()
			cursor.execute(f'SELECT * FROM `dccon` WHERE `id` = \'{dcConName}\'')
			searchResult = cursor.fetchone()
			if(searchResult != None):
				await context.channel.send(searchResult[len(searchResult)-1])
			else:
				log('+09:00', 0, f'"{dcConName}" is not a registered dccon name @ "'+getLocation(context)+'"')

app.run(TOKEN)

# TODO: 테그별로 디씨콘 리스트 출력, 등록된 디씨콘 사진 저장소로 이동 및 중복 사진 삭제, 디씨콘 검색 후 출력, 등 기능 추가