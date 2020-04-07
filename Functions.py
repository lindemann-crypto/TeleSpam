#Functions
try:
	import os
	import json
	import time
	from colorama import Fore
	from colorama import Style
	import telethon
	from telethon.tl.functions.messages import GetHistoryRequest
	from telethon.tl.functions.messages 		import GetDialogsRequest
	from telethon.tl.types import ChannelParticipantsSearch
	from telethon.tl.functions.channels import GetParticipantsRequest
	from telethon.tl.types import ChannelParticipantsSearch
except ModuleNotFoundError as e:
	os.system('pip3 install colorama')
	os.system('pip3 install telethon')
	os.system('clear')


def getInput(text, answers='?', test=True):
	inp = input( Fore.CYAN + "\n[ ? ] " + Fore.GREEN + str(text)+ "[" + '/'.join(str(answer) for answer in answers) + "]" + ": " + Style.RESET_ALL)
	if inp == '.':
		exit()
	if test == True:
		while not inp in answers:
			inp = input(Fore.RED+'[ - ] Please input correct:'+Style.RESET_ALL)
			if inp == '.':
				exit()
	if test == 'int':
		while not inp.isdigit():
			inp = input(Fore.RED+'[ - ] Please input correct:'+Style.RESET_ALL)
			if inp == '.':
				exit()
	if test == 'url/link':
		while not '.' in inp and not '/' in inp:
			inp = input(Fore.RED+'[ - ] Please input correct link:'+Style.RESET_ALL)
			if inp == '.':
				exit()
	if test == 'url/link':
		if not inp.startswith('http'):
			inp = 'https://'+inp
			if inp == '.':
				exit()
	return inp

def printf(num,text):
	print(Fore.CYAN+f'[ {num} ] '+Fore.GREEN+text+Style.RESET_ALL)

def getBanner():
	print(""" ___ ____ _    ____ ____ ___  ____ _  _ 
  |  |___ |    |___ [__  |__] |__| |\/| 
  |  |___ |___ |___ ___] |    |  | |  | 
                                        

""")
	print(Fore.YELLOW+'_'*43+Style.RESET_ALL)
	print(f"@wannadeauth {'_'*5}&&{'_'*5} @wannadeauth_chat")
	print(Fore.YELLOW+f"{'_'*43}\n\tИспользуйте '.' для выхода"+Style.RESET_ALL)
	print('\n\n')
	
def getUserData(user_data_file):
	if os.path.isfile(user_data_file):
		try:
			with open(user_data_file,'r') as data:
				global user_data
				user_data = json.load(data)
		except Exception as e:
			user_data = None
	else:
		user_data = None
	
	if user_data == None:
		os.system('clear')
		getBanner()
		
		api_id = getInput('API_ID',test=False)
		api_hash = getInput('API_HASH',test=False)
		app_title = getInput('APP_TITLE',test=False)
		with open(user_data_file,'w') as file:
			json.dump({ 'API_ID': api_id,
										'API_HASH': api_hash,
										'APP_TITLE': app_title}, file)
		return {'API_ID':api_id, 'API_HASH': api_hash, 'APP_TITLE': app_title}
	else:
		return user_data

def retryGetUserData(user_data_file):
	open(user_data_file,'w')
	#Отчистим файл
	getUserData(user_data_file)
	#Данные запишутся



def printError(Error):
	Error = str(Error)
	if Error.endswith('.'):
		Error = Error[:-1]
	print(f'\n{Fore.RED}[ ! ] {str(Error)}{Style.RESET_ALL}.')
	time.sleep(1.75)

def saveMembers(members_file, members):
	with open(members_file,'w') as file:
		json.dump(members,file)

async def getMembersWithoutAdmin(members_file, channel, client):
	count = 1
	os.system('clear')
	getBanner()
	need_count = getInput('Сколько пользователей необходимо получить?',test = 'int')
	offset_msg = 0    # номер записи, с которой начинается отсчёт
	limit_msg = 100   # максимальное число записей, передаваемых за один раз
	users = []

	while True:
		history = await client(GetHistoryRequest(
			peer=channel,
			offset_id=offset_msg,
			offset_date=None, add_offset=0,
			limit=limit_msg, max_id=0, min_id=0,
			hash=0))
		messages = history.messages
		if not history.messages:
			print('Сообщения закончились.')
			time.sleep(3)
			break
		if count >= int(need_count):
			print('Готово.')
			time.sleep(3)
			break
		for participant in history.users:
			if participant.bot == False:
				user = {"id": participant.id,
					"first_name": participant.first_name,
					"last_name": participant.last_name,
					"user": participant.username,
					"phone": participant.phone,
					"is_bot": participant.bot,
					'access_hash': participant.access_hash}


				if not user in users:
					printf( f'{Fore.GREEN}!{Fore.CYAN}', f'{Fore.GREEN}Получен пользователь id{user["id"]} ({count})')
					time.sleep(0.1)
					users.append(user)
					count += 1
		offset_msg += 100
	with open(members_file, 'w') as f:
		json.dump(users,f)

async def getMembers(members_file, channel,client):
	
	offset_user = 0    # номер участника, с которого начинается считывание
	limit_user = 100   # максимальное число записей, передаваемых за один раз

	all_participants = []   # список всех участников канала
	filter_user = ChannelParticipantsSearch('')

	while True:
		participants =  await client(GetParticipantsRequest(channel,
			filter_user, offset_user, limit_user, hash=0))
		if not participants.users:
			break
		all_participants.extend(participants.users)
		offset_user += len(participants.users)

	all_users = []   # список словарей с интересующими параметрами участников канала

	for participant in all_participants:
		if participant.bot == False:
			print(Fore.GREEN+'[ ! ] Получен пользователь id{id}'+Style.RESET_ALL)
			all_users.append({"id": participant.id,
				"first_name": participant.first_name,
				"last_name": participant.last_name,
				"user": participant.username,
				"phone": participant.phone,
				"is_bot": participant.bot,
				'access_hash': participant.access_hash})

	with open(members_file,'w') as f:
		json.dump(all_users,f)
	print('Готово.')
	time.sleep(3)

async def scrapperMain(members_file,url, adm_request,client):
	channel = await client.get_entity(url)
	if adm_request == 'n':
		await getMembersWithoutAdmin(members_file,channel,client)
	if adm_request == 'y':
		await getMembers(members_file,channel,client)