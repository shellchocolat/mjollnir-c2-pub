#!/usr/bin/python3

import pyfiglet
import sys
import os
import termtables as tt
import threading
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from base64 import b64decode, b64encode
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import CompleteStyle, prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import HTML, FormattedText
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit.styles import Style
from prompt_toolkit import PromptSession
folder = os.path.dirname(os.path.abspath(__file__))+ "/lib/"
sys.path.append(folder)
import helper
import commander
import menus
import viewer
import json
import requests
import getpass

print = print_formatted_text

global WIDE_SPACE, SPACE
WIDE_SPACE = ('', '     ')
SPACE = ('',' ')

##################################################################
# key binding
##################################################################
bindings = KeyBindings()
@bindings.add('c-z')
def _(event):
	" Say 'hello' when `c-z` is pressed. "
	def print_hello():
		print('hello world')
	run_in_terminal(print_hello)

@bindings.add('c-x')
def _(event):
	" Exit when `c-x` is pressed. "
	event.app.exit()


##################################################################
# style
##################################################################
global style, message
style = Style.from_dict({
	# User input (default text).
	'':          '#00aa00', #'#ff0066',

	# Prompt.
	'etk': '#ff0066',
	'end': '#ff0066'
})
message = [
	('class:etk', 'Mjollnir'),
	('class:end', ' > ')
]

##################################################################
# main menu
##################################################################
main_commands = [
	'mission', 'listener', 'agent', 'task', 'r-task', 'g-task', 'launcher', 'login', 'logout', 'first_user', 'help', 'exit',
	# ...
]

main_command_family = {
	'help': ':h',
	'exit': ':q',
}

main_family_colors = {
	'x86/x64': 'ansimagenta',
	'x86': 'ansigreen',
	'x64': 'ansired',
	'x86-64': 'ansiyellow',
	# ...
}

main_meta = {
	'mission': HTML('Create/Edit/Delete/Select a mission and List all missions (-c, -e, -d, -s, -l) Example: <i>mission -c evilcorp</i>'),
	'listener': HTML('Use a listener and List all actives listeners (-u, -l) Example: <i>listener -u listener_name</i> / <i>listener -l</i>'),
	'agent': HTML('Use/Interact with an agent and List all actives agents (-u, -i, -l) Example: <i>agent -u agent_name</i> / <i>agent -l</i>'),
	'task': HTML('Result for a task (-r) Example: <i>task -r task_uid</i>'),
	'r-task': HTML('Create a "on registering task" for an agent_name (-c) Example: <i>r-task agent_name</i>'),
	'g-task': HTML('Create a "group task" for an agent_group (-c) Example: <i>g-task agent_group</i>'),
	'login': HTML('Login to the Mjollnir-api Example: <i>login username</i>'),
	'first_user': HTML('Used to register the first user (can only be used once)'),
	#'list-payloads': HTML('Example: <i>list-payloads</i> / <i>:lspld x86</i> / <i>:lspld windows</i>'),
	#'list-packers': HTML('Example: <i>list-packers</i> / <i>:lspkr x86</i> / <i>:lspkr windows</i>'),
	#'list-encoders': HTML('Example: <i>list-encoders</i> / <i>:lsenc x86</i> / <i>:lsenc windows</i>'),
	'exit': HTML('Exit Mjollnir'),
	#'use': HTML('Example: <i>use shellcode</i> / <i>:u shellcode</i> and interact with it setting its <ansigreen>CMD/RHOST/LHOST/...</ansigreen>'),
	# ...
}

##################################################################
# agent menu
##################################################################

agent_commands =[
	'set', 'generate', 'info', 'back', 'list'
]

agent_commands += main_commands

agent_command_family = {
	'help': ':h',
	'exit': ':q',
}

agent_family_colors = {
	'x86/x64': 'ansimagenta',
	'x86': 'ansigreen',
	'x64': 'ansired',
	'x86-64': 'ansiyellow',
	# ...
}

agent_meta = {
	'generate': HTML('Generate the agent following the procedure inside the config file'),
	'set': HTML('Example: <i>set ip 127.0.0.1</i>'),
	'back': HTML('Return to the previous menu.'),
	'info': HTML('Display some infos about the selected agent'),
	'list': HTML('List all availables agents'),
	# ...
}

##################################################################
# agent interaction menu
##################################################################

agent_interaction_commands =[
	'info', 'back', 'group'
]

agent_interaction_commands += main_commands

agent_interaction_command_family = {
	'help': ':h',
	'exit': ':q',
}

agent_interaction_family_colors = {
	'x86/x64': 'ansimagenta',
	'x86': 'ansigreen',
	'x64': 'ansired',
	'x86-64': 'ansiyellow',
	# ...
}

agent_interaction_meta = {
	'back': HTML('Return to the previous menu.'),
	'info': HTML('Display some nice info about the agent'),
	'group': HTML('Edit agent group. Example: <i>group new_group</i>'),
	# ...
}

##################################################################
# listener menu
##################################################################

listener_commands =[
	'set', 'start', 'info', 'back', 'list'
]

listener_commands += main_commands

listener_command_family = {
	'help': ':h',
	'exit': ':q',
}

listener_family_colors = {
	'x86/x64': 'ansimagenta',
	'x86': 'ansigreen',
	'x64': 'ansired',
	'x86-64': 'ansiyellow',
	# ...
}

listener_meta = {
	'start': HTML('Start the listener'),
	'set': HTML('Example: <i>set ip 127.0.0.1</i>'),
	'back': HTML('Return to the previous menu.'),
	'info': HTML('Display some infos about the selected agent'),
	'list': HTML('List all availables listeners'),
	# ...
}

##################################################################
# on registering task menu
##################################################################

registering_task_commands =[
	'list', 'delete', 'back'
]

registering_task_commands += main_commands

registering_task_command_family = {
	'help': ':h',
	'exit': ':q',
}

registering_task_family_colors = {
	'x86/x64': 'ansimagenta',
	'x86': 'ansigreen',
	'x64': 'ansired',
	'x86-64': 'ansiyellow',
	# ...
}

registering_task_meta = {
	'back': HTML('Return to the previous menu.'),
	'delete': HTML('Delete a task. Example: <i>delete task_uid</i>'),
	'list': HTML('List all availables on registering task'),
	# ...
}

##################################################################
# group task menu
##################################################################

group_task_commands =[
	'list', 'delete', 'back'
]

group_task_commands += main_commands

group_task_command_family = {
	'help': ':h',
	'exit': ':q',
}

group_task_family_colors = {
	'x86/x64': 'ansimagenta',
	'x86': 'ansigreen',
	'x64': 'ansired',
	'x86-64': 'ansiyellow',
	# ...
}

group_task_meta = {
	'back': HTML('Return to the previous menu.'),
	'delete': HTML('Delete a task. Example: <i>delete task_uid</i>'),
	'list': HTML('List all availables agents'),
	# ...
}

def displayContent(content_lst):
	for c in content_lst:
		print(FormattedText([
			WIDE_SPACE, c
			]))
	return True

def bottom_toolbar(value):
	return HTML(' %s'%value)

def main():
	#main_menu = True
	#agent_menu = False
	mjollnir_menus = {
		"main_menu": True, 
		"agent_menu": False,
		"agent_interaction_menu": False,
		"registering_task_menu": False,
		"group_task_menu": False
		}
	value_toolbar = "<b><style bg='ansired'>/</style></b>"
	while 1: 
		# Multi-column menu.
		if mjollnir_menus["main_menu"] == True:
			comp = viewer.AutoCompletion(main_commands, main_command_family, main_family_colors, main_meta)
			userInput = prompt(message, history=FileHistory("history.txt"), auto_suggest=AutoSuggestFromHistory(), completer=comp, complete_style=CompleteStyle.MULTI_COLUMN, style=style, bottom_toolbar=bottom_toolbar(value_toolbar), key_bindings=bindings)
		#userInput = prompt(message, auto_suggest=AutoSuggestFromHistory(), completer=comp, complete_style=CompleteStyle.MULTI_COLUMN, style=style, bottom_toolbar=bottom_toolbar(''), key_bindings=bindings)
		#elif listener_menu:
		#    comp = viewer.AutoCompletion(shellcode_commands, shellcode_command_family, shellcode_family_colors, shellcode_meta)
		#    userInput = prompt(message, history=FileHistory("history.txt"),auto_suggest=AutoSuggestFromHistory(), completer=comp, complete_style=CompleteStyle.MULTI_COLUMN, style=style, bottom_toolbar=bottom_toolbar(shellcode), key_bindings=bindings)
		elif mjollnir_menus["agent_menu"] == True:
			comp = viewer.AutoCompletion(agent_commands, agent_command_family, agent_family_colors, agent_meta)
			userInput = prompt(message, history=FileHistory("history.txt"),auto_suggest=AutoSuggestFromHistory(), completer=comp, complete_style=CompleteStyle.MULTI_COLUMN, style=style, bottom_toolbar=bottom_toolbar(value_toolbar), key_bindings=bindings)
		elif mjollnir_menus["agent_interaction_menu"] == True:
			comp = viewer.AutoCompletion(agent_interaction_commands, agent_interaction_command_family, agent_interaction_family_colors, agent_interaction_meta)
			userInput = prompt(message, history=FileHistory("history.txt"),auto_suggest=AutoSuggestFromHistory(), completer=comp, complete_style=CompleteStyle.MULTI_COLUMN, style=style, bottom_toolbar=bottom_toolbar(value_toolbar), key_bindings=bindings)
		elif mjollnir_menus["listener_menu"] == True:
			comp = viewer.AutoCompletion(listener_commands, listener_command_family, listener_family_colors, listener_meta)
			userInput = prompt(message, history=FileHistory("history.txt"),auto_suggest=AutoSuggestFromHistory(), completer=comp, complete_style=CompleteStyle.MULTI_COLUMN, style=style, bottom_toolbar=bottom_toolbar(value_toolbar), key_bindings=bindings)
		elif mjollnir_menus["registering_task_menu"] == True:
			comp = viewer.AutoCompletion(registering_task_commands, registering_task_command_family, registering_task_family_colors, registering_task_meta)
			userInput = prompt(message, history=FileHistory("history.txt"),auto_suggest=AutoSuggestFromHistory(), completer=comp, complete_style=CompleteStyle.MULTI_COLUMN, style=style, bottom_toolbar=bottom_toolbar(value_toolbar), key_bindings=bindings)
		elif mjollnir_menus["group_task_menu"] == True:
			comp = viewer.AutoCompletion(group_task_commands, group_task_command_family, group_task_family_colors, group_task_meta)
			userInput = prompt(message, history=FileHistory("history.txt"),auto_suggest=AutoSuggestFromHistory(), completer=comp, complete_style=CompleteStyle.MULTI_COLUMN, style=style, bottom_toolbar=bottom_toolbar(value_toolbar), key_bindings=bindings)
			

		if len(userInput) > 1:
			argInput = userInput.split()
			cmd = argInput[0]
		else:
			cmd = ""

		#if (cmd == "use" or cmd == ":u") and len(argInput) == 2:
		#    #r = usePayloadMenu(argInput[1])
		#    #if not r:
		#    #    print("[-] " + argInput[1] + " is not available")
		#    main_menu = False
		#    agent_menu = True
		#    shellcode = argInput[1]
		
		# COMMON COMMANDS
		if cmd.lower() == "help" or cmd.lower() == ':h':
			if len(argInput) == 1: # there is just cmd without any command
				helper.helpMenu('')
			else:
				helper.helpMenu(argInput[1])
		elif cmd.lower() == 'back' or cmd.lower() == ":b":
			mjollnir_menus["main_menu"] = True
			mjollnir_menus["agent_menu"] = False
			mjollnir_menus["agent_interaction_menu"] = False
			mjollnir_menus["listener_menu"] = False
			mjollnir_menus["registering_task_menu"] = False
			mjollnir_menus["group_task_menu"] = False
			global_agent_name = ""
			global_agent_uid = ""
			global_listener_name = ""
			global_group_name = ""
			value_toolbar = "<b><style bg='ansired'>/</style></b>"
		elif cmd.lower() == "exit" or cmd.lower() == ':q':
			sys.exit(0)
		elif cmd.lower() == "first_user":
			commander.manage_first_user()
		elif cmd.lower() == "login":
			commander.manage_login(argInput)
		elif cmd.lower() == "logout":
			commander.manage_logout()
		elif cmd.lower() == "user":
			if len(argInput) == 1:
				# go to user menu
				pass
			else:
				commander.manage_user(argInput)
		elif cmd.lower() == "agent":
			mjollnir_menus["main_menu"] = False
			mjollnir_menus["listener_menu"] = False
			mjollnir_menus["registering_task_menu"] = False
			mjollnir_menus["group_task_menu"] = False
			if len(argInput) == 1:
				mjollnir_menus["agent_menu"] = True
				mjollnir_menus["agent_interaction_menu"] = False
				value_toolbar = "<b><style bg='ansired'> AGENT: %s</style></b>"%("")
			elif len(argInput) >= 3 and argInput[1] == "-i":
				mjollnir_menus["agent_menu"] = False
				mjollnir_menus["agent_interaction_menu"] = True
				global_agent_uid = argInput[2]
				value_toolbar = "<b><style bg='ansired'> AGENT INTERACTION: %s</style></b>"%global_agent_uid
			elif len(argInput) >= 3 and argInput[1] == "-u":
				mjollnir_menus["agent_menu"] = True
				mjollnir_menus["agent_interaction_menu"] = False
				agent_name = argInput[2]
				if menus_agent.menu_agent_use(agent_name):
					global_agent_name = agent_name
				else:
					global_agent_name = ""
				value_toolbar = "<b><style bg='ansired'> AGENT: %s</style></b>"%global_agent_name
			else:
				mjollnir_menus["agent_menu"] = False
				mjollnir_menus["agent_interaction_menu"] = True
				commander.manage_agent(argInput)
		
		elif cmd.lower() == "task":
			if len(argInput) == 1:
				# go to task menu
				pass
			else:
				commander.manage_task(argInput)

		elif cmd.lower() == "r-task":
			mjollnir_menus["main_menu"] = False
			mjollnir_menus["agent_menu"] = False
			mjollnir_menus["agent_interaction_menu"] = False
			mjollnir_menus["listener_menu"] = False
			mjollnir_menus["registering_task_menu"] = True
			mjollnir_menus["group_task_menu"] = False
			if len(argInput) == 1:
				global_agent_name = input("agent name: ")
				value_toolbar = "<b><style bg='ansired'> ON REGISTERING TASK: %s</style></b>"%global_agent_name
			elif len(argInput) >= 2:
				global_agent_name = argInput[1]
				value_toolbar = "<b><style bg='ansired'> ON REGISTERING TASK: %s</style></b>"%global_agent_name
			else:
				mjollnir_menus["main_menu"] = True
				mjollnir_menus["registering_task_menu"] = False
				global_agent_name = ""

		elif cmd.lower() == "g-task":
			mjollnir_menus["main_menu"] = False
			mjollnir_menus["agent_menu"] = False
			mjollnir_menus["agent_interaction_menu"] = False
			mjollnir_menus["listener_menu"] = False
			mjollnir_menus["registering_task_menu"] = False
			mjollnir_menus["group_task_menu"] = True
			if len(argInput) == 1:
				global_group_name = input("group name: ")
				value_toolbar = "<b><style bg='ansired'> GROUP TASK: %s</style></b>"%global_group_name
			elif len(argInput) >= 2:
				global_group_name = argInput[1]
				value_toolbar = "<b><style bg='ansired'> GROUP TASK: %s</style></b>"%global_group_name
			else:
				mjollnir_menus["main_menu"] = True
				mjollnir_menus["group_task_menu"] = False
				global_agent_name = ""

		elif cmd.lower() == "mission":
			if len(argInput) == 1:
				# go to mission menu
				pass
			else:
				commander.manage_mission(argInput)
		elif cmd.lower() == "listener":
			mjollnir_menus["main_menu"] = False
			mjollnir_menus["agent_menu"] = False
			mjollnir_menus["agent_interaction_menu"] = False
			mjollnir_menus["registering_task_menu"] = False
			mjollnir_menus["group_task_menu"] = False
			if len(argInput) == 1:
				mjollnir_menus["listener_menu"] = True
				value_toolbar = "<b><style bg='ansired'> LISTENER: %s</style></b>"%("")
			elif len(argInput) >= 3 and argInput[1] == "-u":
				mjollnir_menus["listener_menu"] = True
				listener_name = argInput[2]
				if menus_listener.menu_listener_use(listener_name):
					global_listener_name = listener_name
				else:
					global_listener_name = ""
				value_toolbar = "<b><style bg='ansired'> LISTENER: %s</style></b>"%global_listener_name
			else:
				mjollnir_menus["listener_menu"] = True
				commander.manage_listener(argInput)  

		# LISTENER MENU
		elif mjollnir_menus["listener_menu"] == True:
			if cmd.lower() == "list":
				menus_listener.menu_listener_list()
			elif cmd.lower() == "start":
				menus_listener.menu_listener_start(global_listener_name)
			elif cmd.lower() == "info":
				menus_listener.menu_listener_info(global_listener_name)
			elif cmd.lower() == "set":
				if len(argInput) >= 2:
					param_value = (argInput[1], argInput[2])  # (IP, 127.0.0.1)
					menus_listener.menu_listener_set(global_listener_name, param_value)
			elif cmd.lower() == "use":
				if len(argInput) >= 2:
					global_listener_name = argInput[1]
				else:
					global_listener_name = input("listener name: ")
				value_toolbar = "<b><style bg='ansired'> LISTENER: %s</style></b>"%global_listener_name
				menus_listener.menu_listener_use(global_listener_name)

		# AGENT MENU
		elif mjollnir_menus["agent_menu"] == True:
			if cmd.lower() == "list":
				menus_agent.menu_agent_list()
			elif cmd.lower() == "generate":
				menus_agent.menu_agent_generate(global_agent_name)
			elif cmd.lower() == "info":
				menus_agent.menu_agent_info(global_agent_name)
			elif cmd.lower() == "set":
				if len(argInput) >= 2:
					param_value = (argInput[1], argInput[2])  # (RHOST, 127.0.0.1)
					menus_agent.menu_agent_set(global_agent_name, param_value)
			elif cmd.lower() == "use":
				if len(argInput) >= 2:
					global_agent_name = argInput[1]
				else:
					global_agent_name = input("agent name: ")
				value_toolbar = "<b><style bg='ansired'> AGENT: %s</style></b>"%global_agent_name
				menus_agent.menu_agent_use(global_agent_name)

		# AGENT INTERACTION MENU
		elif mjollnir_menus["agent_interaction_menu"] == True:
			if cmd.lower() == "info":
				menus_agent_interaction.menu_current_agent_info(global_agent_uid)
			elif cmd.lower() == "group":
				menus_agent_interaction.menu_edit_agent_group(global_agent_uid, argInput)
			elif cmd.lower() == "list":
				menus_agent_interaction.list_task(global_agent_uid)
			else:
				agent_name = menus_agent_interaction.menu_current_agent_name(global_agent_uid)
				agent_commands_interaction = config["agent"]["details"][agent_name]["commands"]
				found = False
				# check if command exist for that agent name
				for k in agent_commands_interaction.keys():
					if cmd.upper() == agent_commands_interaction[k]["name"]:
						found = True
						break
				
				if not found and cmd != "":
					print("[-] That command does not exist (check your config file): " + cmd.upper())
				else:
					menus_agent_interaction.submit_task(global_agent_uid, argInput)

		# ON REGISTERING TASK MENU
		elif mjollnir_menus["registering_task_menu"] == True:
			if cmd.lower() == "list":
				menus_registering_task.registering_task_list(global_agent_name)
			elif cmd.lower() == "delete":
				menus_registering_task.registering_task_delete(argInput)
			else:
				all_agent_commands = config["agent"]["details"][global_agent_name]["commands"]
				found = False
				# check if command exist for that agent name
				for k in all_agent_commands.keys():
					if cmd.upper() == all_agent_commands[k]["name"]:
						found = True
						break

				if not found and cmd != "":
					print("[-] That command does not exist (check your config file): " + cmd.upper())
				else:
					menus_registering_task.registering_task_create(global_agent_name, argInput)


		# GROUP TASK MENU
		elif mjollnir_menus["group_task_menu"] == True:
			if cmd.lower() == "list":
				pass
				#menus_group_task.group_task_list(global_group_name)
			elif cmd.lower() == "delete":
				pass
				#menus_group_task.registering_task_delete(argInput)
			else:
				# can't determine easily if CMD existe because it could have different
				# agent within the same group
					menus_group_task.group_task_create(global_group_name, argInput)
		

def printBanner():
	#ascii_banner = pyfiglet.figlet_format("Exploit Tool Kit")
	#print(ascii_banner)

	# https://github.com/pwaller/pyfiglet/tree/master/pyfiglet/fonts
	#custom_ascii = pyfiglet.Figlet(font='cosmic')
	custom_ascii = pyfiglet.Figlet()
	print(FormattedText([
		('ansiblue', custom_ascii.renderText("Mjollnir c2"))
		]))
	return True

if __name__ == '__main__':
	printBanner()
	print()

	with open("../config.json", "r") as fp:
		config = fp.read()
	config = json.loads(config)
	#print(config)

	s = requests.session()
	s.proxies = {
		"http": config["proxy_mjollnir_cli"]["http"],
		"https": config["proxy_mjollnir_cli"]["https"],
	}

	commander = commander.Commander(config, s)
	helper = helper.Helper()
	menus_agent = menus.Agent(config, s)
	menus_agent_interaction = menus.AgentInteraction(config, s)
	menus_listener = menus.Listener(config, s)
	menus_registering_task = menus.OnRegisteringTask(config, s)
	menus_group_task = menus.GroupTask(config, s)

	global global_agent_name, global_agent_uid, global_listener_name, global_group_name
	global_agent_name = ""
	global_agent_uid = ""
	global_listener_name = ""
	global_group_name = ""

	global session
	session = PromptSession()

	global selected_agent
	selected_agent = ""

	main()
