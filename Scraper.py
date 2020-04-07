#Scraper
try:
	try:
		import os
		from Functions import *
		import colorama
		from telethon import TelegramClient
		from telethon.errors.rpcerrorlist import ApiIdInvalidError
	except ModuleNotFoundError as e:
		os.system('pip3 install colorama')
		os.system('pip3 install telethon')
		os.system('clear')
	
	user_data_file = 'user_data.json'
	members_file = 'members.json'
	
	try:
		user_data = getUserData(user_data_file)
		api_id = user_data['API_ID']
		api_hash = user_data['API_HASH']
		app_title = user_data['APP_TITLE']
		try:
			client = TelegramClient(app_title, api_id, api_hash)
			auth = True
		except ValueError:
			auth = False
			retryGetUserData(user_data_file)
		os.system('clear')
		getBanner()
		url = getInput(f"Введите пригласительную ссылку\n{colorama.Fore.YELLOW}[ * ] Можно получить участников канала если вы администратор\n[ * ] Участников чата можно получить без прав администратора{colorama.Fore.CYAN}\n\nlink:", test = "url/link")
		adm_request = getInput('Вы админ?',['n','y'])
		if auth == True:
			try:
				with client:
					client.loop.run_until_complete(scrapperMain(members_file, url, adm_request, client))
			except ConnectionError as e:
				os.system('clear')
				getBanner()
				printError(e)
				exit()
			except ApiIdInvalidError or TypeError:
				os.system('clear')
				getBanner()
				printError('Плоxие данные.')
				retryGetUserData(user_data_file)
	except AttributeError as e:
		printError(e)

except KeyboardInterrupt:
	printError(f'{colorama.Fore.YELLOW}Операция прерванна.')