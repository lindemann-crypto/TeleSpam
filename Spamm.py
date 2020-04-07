try:
	try:
		import os
		from Functions import *
		from colorama import *
		import telethon
		from telethon.tl.functions.messages import GetDialogsRequest
		from telethon.tl.types import InputPeerEmpty
		from telethon.sync import TelegramClient
		from telethon.errors.rpcerrorlist import PeerFloodError, ApiIdInvalidError
		from telethon.tl.types import InputPeerUser
	except ModuleNotFoundError:
		os.system('pip3 install telethon')
		os.system('pip3 install colorama')
	
	user_data_file = 'user_data.json'
	members_file = 'members.json'
	
	
	while True:
		#Main menu
		os.system('clear')
		getBanner()
		printf( 1 , 'Начать спаминг.')
		printf( 2 , 'Настроить спаммер.')
		printf( 3 ,'Выйти.')
		
		mode = int( getInput( 'Режим', ['1','2','3']) )
		if mode == 3:
			time.sleep(0.5)
			exit()
	
		user_data = getUserData(user_data_file)
		api_id = user_data['API_ID']
		api_hash = user_data['API_HASH']
		app_title = user_data['APP_TITLE']
		try:
			client = TelegramClient(app_title, api_id, api_hash)
			client.connect()
	
			if not client.is_user_authorized():
				phone = getInput('Моб. телефон', test=False)
				client.send_code_request(phone)
		except ConnectionError:
			printError('ОШИБКА СОЕДЕНЕНИЯ')
			exit()
		except TypeError or ApiIdInvalidError:
			os.system('clear')
			getBanner()
			printError('Не верные данные')
			retryGetUserData(user_data_file)
			continue
	
			os.system('clear')
			getBanner()
			client.sign_in(phone, getInput('Код из смс',test=False))
		
		if mode == 1:
			if os.path.isfile(members_file):
				try:
					with open(members_file,'r') as file:
						#global members
						members = json.load(file)
				except Exception as e:
					members = None
					printError(e)
	
			else:
				members = None
				printError( 'Файл с данными пользователей не был создан')
				printError('Перейдите к пункту 2' )
			
			if members != None:
				os.system('clear')
				getBanner()
				printf( 1 , 'Рассылка по айди(больше).')
				printf( 2 , 'Рассылка по ник-нейму.')
				
				spam_mode = getInput( 'Режим', ['1','2'])
				os.system('clear')
				getBanner()
				Banner = input(Fore.YELLOW+f'[ * ] Когда закончите банер напишите в новую строку "."\n{Fore.GREEN}[ ? ]Введите ваш банер: {Style.RESET_ALL}')
				inp = ''
				while inp != '.':
					inp = input(Fore.GREEN+'[ ? ] Новая строка: '+Style.RESET_ALL)
					if inp != '.':
						Banner = Banner + f"\n{inp}"
	
				os.system('clear')
				getBanner()
				print(f'Ваш банер:\n{Banner}\n')
				
				i = 1
				if spam_mode == '1':
					for member in members:
						try:
							receiver = InputPeerUser(member['id'],member['access_hash'])
							client.send_message(receiver, Banner)
							printf( '+' , f'Сообщение отправленно id{id} ({i})')
							i += 1
						except Exception as e:
							printError(e)
							if e == PeerFloodError:
								printError('Ваш аккаунт был помещён в спам')
								exit()
	
				if spam_mode == '2':
					for member in members:
						try:
							client.send_message(member['username'], Banner)
							printf( '+' , f'Сообщение отправленно name = {name} ({i})')
							i += 1
						except Exception as e:
							printError(e)
							if e == PeerFloodError:
								exit()
	
		if mode == 2:
			os.system('clear')
			getBanner()
			reset = getInput( f'{Fore.RED}СБРОСИТЬ НАСТРОЙКИ?{Style.RESET_ALL}',['n','y'])
			if reset == 'n':
				continue
			elif reset == 'y':
				retryGetUserData(user_data_file)
except KeyboardInterrupt:
	printError(f'{colorama.Fore.YELLOW}Операция прерванна.')	