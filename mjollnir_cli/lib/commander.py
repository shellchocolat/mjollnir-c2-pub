import os
import sys
sys.path.insert(0,'../')
import sqlite3
from base64 import b64encode, b64decode
import json
import termtables as tt
import getpass
import agent
import user
import mission
import listener
import task
import misc

"""
.. moduleauthor:: shellchocolat <shellchocolat@no-mail.com>
"""

class Commander(object):
	"""This class is used to handle the command that the user could do.
	"""
	def __init__(self, config, session):
		self.config = config
		self.s = session
		self.misc = misc.Misc()
		self.agent = agent.Agent(self.config, self.s, self.misc)
		self.user = user.User(self.config, self.s, self.misc)
		self.mission = mission.Mission(self.config, self.s, self.misc)
		self.listener = listener.Listener(self.config, self.s, self.misc)
		self.task = task.Task(self.config, self.s, self.misc)

	def manage_first_user(self):
		username = input("username: ")
		password = getpass.getpass(prompt='password: ')
		self.user.first_user(username, password)

	def manage_logout(self):
		self.user.user_logout()

	def manage_login(self, argInput):
		self.user.user_login(argInput)

	def manage_user(self, argInput):
		L = len(argInput)
		action = argInput[1]
		if action == "-l": # list all users
			if L >= 2:
				self.user.list_users()

	def manage_download(self, argInput):
		L = len(argInput)
		if L >= 3:
			source = argInput[1]
			destination = argInput[2]
			self.agent.download_agent(source, destination)
		else:
			print("[-] Need a source and a destination")
			print("[*] download http://127.0.0.1/public/agent.exe /tmp/agent.exe")
				
	def manage_agent(self, argInput):
		L = len(argInput)
		action = argInput[1]
		
		if action == "-l": # list all agents
			if L >= 2:
				self.agent.list_agents()

		elif action == "-d": # delete an agent
			if L >= 3:
				#agents_uid = argInput[2]
				agents_uid = []
				for i in range(2, L):
					agents_uid.append(argInput[i])
				self.agent.delete_agent(agents_uid)
				self.task.delete_all_tasks_for_agent(agents_uid)
		elif action == "-i": # interact with an agent
			if L >= 3:
				agent_uid = argInput[2]
				self.agent.interact_agent(agent_uid)
			else:
				print("[-] Need a user uid: agent -i <agent_uid>")
		else:
			print("[-] Action not found: " + action)

	def manage_task(self, argInput):
		L = len(argInput)
		action = argInput[1]
		if action == "-r": # get result for a task
			if L >= 3: # task -r task_uid
				task_uid = argInput[2]
				self.task.get_result("", task_uid)
			else:
				print("[-] Need a task uid: task -r <task_uid>")

		else:
			print("[-] Action not found: " + action)
				
	def manage_mission(self, argInput):
		L = len(argInput)
		action = argInput[1]
		
		if action == "-l": # list all missions
			if L == 2:
				self.mission.list_missions()

		elif action == "-s": # select a mission
			if L >= 3:
				mission_uid = argInput[2]
				self.mission.select_mission(mission_uid)
			else:
				print("[-] Need a mission uid: mission -s <mission_uid>")

		elif action == "-c": # create a mission
			if L >= 3:
				mission_name = argInput[2]
				self.mission.create_mission(mission_name)
			else:
				print("[-] Need a mission name: mission -c <mission_name>")

		elif action == "-e": # edit a mission
			if L >= 3:
				print()

		elif action == "-d": # delete a mission
			if L >= 3:
				#mission_uid = argInput[2]
				missions_uid = []
				for i in range(2, L):
					missions_uid.append(argInput[i])
				self.mission.delete_mission(missions_uid)
			else:
				print("[-] Need a mission uid: mission -d <mission_uid>")
				
		else:
			print("[*] Action not found: " + action)

	def manage_listener(self, argInput):
		L = len(argInput)
		action = argInput[1]
		
		if action == "-l": # list all listeners
			if L >= 2:
				self.listener.list_listeners()

		elif action == "-d": # delete a listener
			if L >= 3:
				#listener_uid = argInput[2]
				listeners_uid = []
				for i in range(2, L):
					listeners_uid.append(argInput[i])
				self.listener.delete_listener(listeners_uid)
			else:
				print("[-] Need a listener uid: listener -d <listener_uid>")

			
		elif action == "-c": # create a listener
			if L >= 5:
				self.listener.create_listener(argInput)
			else:
				print("[-] Miss some parameters ...")

		else:
			print("[-] Action not found: " + action)


					


