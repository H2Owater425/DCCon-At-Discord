#-*- coding:utf-8 -*-
import asyncio, discord, json, pymysql, re
from dotenv import load_dotenv
from library.apachelog import ApacheLog
from math import ceil
from os import getenv

load_dotenv(verbose=True, encoding='utf-8')

BOT_TOKEN = getenv('BOT_TOKEN')
BOT_PREFIX = getenv('BOT_PREFIX')
BOT_SUB_PREFIX = getenv('BOT_SUB_PREFIX')
BOT_COMMAND = {
	'system': {
		'help': {
			'name': '도움말', 'description': f'`{BOT_PREFIX}도움말`', 'command': f'{BOT_PREFIX}도움말', 'argument': False
		},
		'list': {
			'name': '콘목록', 'description': f'`{BOT_PREFIX}콘목록 <태그|페키지>`', 'command': f'{BOT_PREFIX}콘목록', 'argument': True
		}
	},
	'dccon': {
		'registered_dccon': {
			'name': '등록된 디씨콘', 'description': f'`{BOT_SUB_PREFIX}<별칭>`', 'command': None, 'argument': False
		},
		'unregistered_dccon': {
			'name': '미등록된 디씨콘', 'description': f'`{BOT_SUB_PREFIX}<패키지> <번호|이름>`', 'command': None, 'argument': False
		}
	}
}
PEPRE_COLOR = 0x5c7fd1
DATABASE = json.loads(getenv('DATABASE').replace('\'', '"'))
log = ApacheLog(export=getenv('LOG_FILE_PATH')).log

class Client(discord.Client):
	def fetchDatabaseData(self, query: str, bind_parameter: tuple=()):
		query = re.sub(r'(?<!\\)\?', r'%s', query)
		database = pymysql.connect(host=DATABASE['host'], port=DATABASE['port'], user=DATABASE['user'], password=DATABASE['password'], database=DATABASE['database'], charset='utf8', cursorclass=pymysql.cursors.DictCursor)
		cursor = database.cursor()

		cursor.execute(query, bind_parameter)

		queryResult = cursor.fetchall()

		database.close()
		
		if(len(queryResult) == 1):
			return queryResult[0]

		else:
			return queryResult
	
	def getLocation(self, _object: object):
		try:
			guild = _object.guild
			channel = _object.channel
			user = _object.author

		except AttributeError:
			guild = self.get_guild(_object.guild_id)
			channel = self.get_channel(_object.channel_id)
			user = self.get_user(_object.user_id)

		return f'{guild.name} > {channel.name} > {user.name}'



	async def on_ready(self):
		# When bot started

		try:
			log('+09:00', 1, f'Logged in discord as {self.user.name}({self.user.id}) @ DISCORD')

			await self.change_presence(status=discord.Status.online, activity=discord.Game(f'{BOT_COMMAND["system"]["help"]["command"]} / 물워터#7826'))

			self.fetchDatabaseData('SELECT 1')

			log('+09:00', 1, f'Logged in database as {DATABASE["user"]} @ DATABASE("{DATABASE["host"]}")')

		except Exception as error:
			log('+09:00', 6, 'Error: '+str(error).replace('\n', '; ')+' @ SYSTEM')

			return exit()

	async def on_message(self, context):
		try:
			if(context.author.bot):
				return 0
			
			command, argument = context.content.split(' ')[0], context.content.split(' ')[1:]
			
			if(command == BOT_COMMAND['system']['help']['command']):
				# ~!도움말
				
				embed = discord.Embed().from_dict({
					'title': 'DCCon@Discord | Commands',
					'color': PEPRE_COLOR,
					'thumbnail': {
						'url': 'https://cdn.discordapp.com/avatars/786819317991211029/6fc5ec0a07c858ad1c3e48bda1a0a372.png?size=128'
					},
					'fields': [
						{ 
							'name': BOT_COMMAND['dccon']['registered_dccon']['name'],
							'value': BOT_COMMAND['dccon']['registered_dccon']['description'],
							'inline': True
						},
						{ 
							'name': BOT_COMMAND['dccon']['unregistered_dccon']['name'],
							'value': BOT_COMMAND['dccon']['unregistered_dccon']['description'],
							'inline': True
						},
						{ 
							'name': '\u200b',
							'value': '\u200b',
							'inline': True
						},
						{ 
							'name': BOT_COMMAND['system']['help']['name'],
							'value': BOT_COMMAND['system']['help']['description'],
							'inline': True
						},
						{ 
							'name': BOT_COMMAND['system']['list']['name'],
							'value': BOT_COMMAND['system']['list']['description'],
							'inline': True
						},
						{ 
							'name': '\u200b',
							'value': '\u200b',
							'inline': True
						}
					]
				})

				await context.channel.send(embed=embed)

				log('+09:00', 1, f'Command excuted: "{command}" @ "{self.getLocation(context)}"')
			
			elif(command == BOT_COMMAND['system']['list']['command']):
				# ~!콘목록 | ~!콘목록 <태그ㅣ패키지>

				if(len(argument) == 0):
					# ~!콘목록

					searchResult = self.fetchDatabaseData(f'SELECT DISTINCT `tag` FROM `{DATABASE["dcConTable"]}` ORDER BY `tag` ASC')
					totalTagCount = len(searchResult)
					totalPageCount = ceil(totalTagCount/10)
					searchResult = searchResult[:10]

					if(len(searchResult) == 0):
						raise Exception('No tag searched from the database')

					tagList = []

					for i in range(len(searchResult)):
						tagList.append(f'**`{i+1}`** {searchResult[i]["tag"]}')

					embed = discord.Embed().from_dict({
						'title': f'All DCCon Tag List ({totalTagCount} Tags)',
						'description': '\n'.join(tagList),
						'color': PEPRE_COLOR,
						'footer': {
							'text': f'Page 1/{totalPageCount}'
						}
					})
					
					message = await context.channel.send(embed=embed)
					
					if(totalPageCount > 1):
						await message.add_reaction("⬅")
						await message.add_reaction("➡")

					log('+09:00', 1, f'Command excuted: "{command}" @ "{self.getLocation(context)}"')

				elif(len(argument) == 1):
					# ~!콘목록 <태그ㅣ패키지>
					dcConTag = pymysql.escape_string(argument[0])
					searchResult = self.fetchDatabaseData(f'SELECT `id`, `url` FROM `{DATABASE["dcConTable"]}`  WHERE `tag` = \'{dcConTag}\' ORDER BY `id` ASC')
					totalTagCount = len(searchResult)
					totalPageCount = ceil(totalTagCount/10)
					searchResult = searchResult[:10]

					if(len(searchResult) == 0):
						raise Exception(f'No tag searched from the database with argument: "{dcConTag}"')

					dcConList = []

					for i in range(len(searchResult)):
						dcConList.append(f'**`{i+1}`** [{searchResult[i]["id"]}]({searchResult[i]["url"]})')

					embed = discord.Embed().from_dict({
						'title': f'DCCon List ({totalTagCount} DCCons)',
						'color': PEPRE_COLOR,
						'fields': [
							{
								'name': dcConTag,
								'value': '\u200b\n'+'\n'.join(dcConList)
							}
						],
						'footer': {
							'text': f'Page 1/{totalPageCount}'
						}
					})
					
					message = await context.channel.send(embed=embed)
					
					if(totalPageCount > 1):
						await message.add_reaction("⬅")
						await message.add_reaction("➡")

					log('+09:00', 1, f'Command excuted: "{command}" @ "{self.getLocation(context)}"')
				
				else:
					raise Exception(f'Too many arguments({len(argument)}) were given to command: "{BOT_COMMAND["system"]["list"]["command"]}"')

			elif(command.startswith(BOT_PREFIX)):
				raise Exception(f'Undefined command: "{command}"')

			elif(command.startswith(BOT_SUB_PREFIX)):
				# ~<별칭> | ~<패키지> <번호|이름>

				if(len(argument) > 0):
					# ~<패키지> <번호|이름>

					pass

				else:
					# ~<별칭>

					dcConName = pymysql.escape_string(command.replace(BOT_SUB_PREFIX, ''))
					searchResult = self.fetchDatabaseData(f'SELECT * FROM `dccon` WHERE `id` = \'{dcConName}\'')

					if(len(searchResult) != 0):
						await context.channel.send(searchResult['url'])

						log('+09:00', 1, f'DCCon sended: "{dcConName}" @ "{self.getLocation(context)}"')

					else:
						raise Exception(f'Unregistered dccon name: "{dcConName}" @ "{self.getLocation(context)}"')
		
		except Exception as error:
			log('+09:00', 5, 'Error: '+str(error).replace('\n', '; ')+f' @ "{self.getLocation(context)}"')
	
	async def on_raw_reaction_add(self, payload):
		try:
			channel = self.get_channel(payload.channel_id)
			message = await channel.fetch_message(payload.message_id)

			if(payload.user_id == self.user.id):
				return 0
			
			elif(not payload.emoji.name in ['⬅', '➡']):
				return 0

			elif(not (message.reactions[0].me and message.reactions[1].me)):
				return 0

			await message.remove_reaction(payload.emoji, payload.member)

			currentPage = int(message.embeds[0].footer.text.replace('Page ', '').split('/')[0])-1

			if(message.embeds[0].title.startswith('All DCCon Tag List (') and message.embeds[0].title.endswith(' Tags)')):
				# 태그 목록

				if(payload.emoji.name == '⬅'):
					if(currentPage-1 != -1):
						currentPage -= 1
					else:
						return 0

				elif(payload.emoji.name == '➡'):
						currentPage += 1

				searchResult = self.fetchDatabaseData(f'SELECT DISTINCT `tag` FROM `{DATABASE["dcConTable"]}` ORDER BY `tag` ASC')
				totalTagCount = len(searchResult)
				totalPageCount = ceil(totalTagCount/10)
				searchResult = searchResult[10*currentPage:10+10*currentPage]

				if(len(searchResult) == 0):
					raise Exception('No tag searched from the database')

				elif(currentPage == totalPageCount):
					return 0

				tagList = []

				for i in range(len(searchResult)):
					tagList.append(f'**`{i+1+10*currentPage}`** {searchResult[i]["tag"]}')

				embed = discord.Embed().from_dict({
					'title': f'All DCCon Tag List ({totalTagCount} Tags)',
					'description': '\n'.join(tagList),
					'color': PEPRE_COLOR,
					'footer': {
						'text': f'Page {currentPage+1}/{totalPageCount}'
					}
				})

				await message.edit(embed=embed)

			elif(message.embeds[0].title.startswith('DCCon List (') and message.embeds[0].title.endswith(' DCCons)')):
				# 디시콘 목록

				if(payload.emoji.name == '⬅'):
					if(currentPage-1 != -1):
						currentPage -= 1
					else:
						return 0

				elif(payload.emoji.name == '➡'):
						currentPage += 1

				dcConTag = message.embeds[0].fields[0].name
				searchResult = self.fetchDatabaseData(f'SELECT `id`, `url` FROM `{DATABASE["dcConTable"]}`  WHERE `tag` = \'{dcConTag}\' ORDER BY `id` ASC')
				totalTagCount = len(searchResult)
				totalPageCount = ceil(totalTagCount/10)
				searchResult = searchResult[10*currentPage:10+10*currentPage]

				if(len(searchResult) == 0):
					raise Exception(f'No tag searched from the database with argument: "{dcConTag}"')

				elif(currentPage == totalPageCount):
					return 0

				dcConList = []

				for i in range(len(searchResult)):
					dcConList.append(f'`{i+1+10*currentPage}` [{searchResult[i]["id"]}]({searchResult[i]["url"]})')

				embed = discord.Embed().from_dict({
					'title': f'DCCon List ({totalTagCount} DCCons)',
					'color': PEPRE_COLOR,
					'fields': [
						{
							'name': dcConTag,
							'value': '\u200b\n'+'\n'.join(dcConList)
						}
					],
					'footer': {
						'text': f'Page {currentPage+1}/{totalPageCount}'
					}
				})

				await message.edit(embed=embed)

		except Exception as error:
			log('+09:00', 5, 'Error: '+str(error).replace('\n', '; ')+f' @ "{self.getLocation(payload)}"')

app = Client()

try:
	app.run(BOT_TOKEN)

finally:
	log('+09:00', 1, f'Application stopped @ SYSTEM')

# TODO: 또또또 리펙토링하기, 미등록 디시콘 검색 및 사용 기능 만들기