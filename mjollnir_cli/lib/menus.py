import os
import sys
sys.path.insert(0,'../')
import sqlite3
import threading
import time
from base64 import b64encode, b64decode
import json
import termtables as tt
import uuid
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

class Agent(object):
	"""This class is used to handle the command that the user could do.
	"""
	def __init__(self, config, session):
		self.config = config
		self.s = session
		self.misc = misc.Misc()
		self.agent_parameters = {}
		self.agent = agent.Agent(self.config, self.s, self.misc)

	def menu_agent_list(self):
		agents = self.config["agent"]
		agents_details= agents["details"]
		agent_details_keys = agents_details.keys()
		headers = ["name", "stages", "info"]
		values = []
		row = []
		for k in agent_details_keys:
			row.append(k)
			row.append(agents_details[k]["stages"]["how_many"])
			row.append(agents_details[k]["info"])
			values.append(row)
			row = []
		
		tt.print(values, header=headers)
		return True
	
	def menu_agent_info(self, agent_name):
		try:
			agents = self.config["agent"]["details"][agent_name]
		except Exception as e:
			#print(str(e))
			print("[-] This agent does not exist: " + agent_name)
			return False

		parameters = agents["parameters"]
		parameters_info = agents["parameters_info"]
		headers = ["PARAMETERS", "VALUES", "INFOS"]
		#headers = parameters
		values = []
		row = []
		#print(self.agent_parameters)
		#print(parameters_info)
		for k in self.agent_parameters.keys():
			row.append(k)
			row.append(self.agent_parameters[k])

			if k in parameters_info.keys():
				row.append(parameters_info[k])
			else:
				row.append("")
			
			values.append(row)
			row = []

		print("\n Name: " + agent_name)
		print(" Info: " + agents["info"])
		print(" How many stages: " + agents["stages"]["how_many"])
		print()
		tt.print(values, header=headers)

		return True

	def menu_agent_generate(self, agent_name):
		try:
			agents = self.config["agent"]["details"][agent_name]
		except Exception as e:
			#print(str(e))
			print("[-] This agent does not exist: " + agent_name)
			return False

		for k in self.agent_parameters.keys():
			if self.agent_parameters[k] == "":
				print("[-] You must fill all the required parameters")
				return False


		param_to_send = {}
		for k in self.agent_parameters.keys():
			if k.upper() == "FRUIT":
				if "yes" in self.agent_parameters[k]:
					param_to_send[k] = str(uuid.uuid4())
				else:
					param_to_send[k] = ""

			elif k.upper() == "LOCATION":
				if "public" in self.agent_parameters[k]:
					param_to_send[k] = self.config["fileserver"]["public_download"]
				else:
					param_to_send[k] = self.config["fileserver"]["private_download"]

			else:
				param_to_send[k] = self.agent_parameters[k]

		param_to_send["agent_name"] = agent_name


		self.agent.generate_agent(agent_name, param_to_send)

		return True


	def menu_agent_set(self, agent_name, param_value):
		# param_value = (param, value) = (RHOST, 127.0.0.1)
		try:
			agents = self.config["agent"]["details"][agent_name]
		except Exception as e:
			#print(str(e))
			print("[-] This agent does not exist: " + agent_name)
			return False

		param = param_value[0]
		if param.upper() in agents["parameters"]:
			self.agent_parameters[param.upper()] = param_value[1]
		else:
			return False

		return True
	
	def menu_agent_use(self, agent_name):
		self.agent_parameters = {}
		# retrieve all the agents name to verify that the name entered by the user exists
		try:
			agents = self.config["agent"]["details"][agent_name]
		except Exception as e:
			#print(str(e))
			print("[-] This agent does not exist: " + agent_name)
			return False

		# retrieve parameters needed for the selected agent
		parameters = agents["parameters"]
		default_parameters = agents["default_parameters"]
		parameters_info = agents["parameters_info"]
		headers = ["PARAMETERS", "VALUES", "INFOS"]
		values = []
		row = []
		for p in parameters:
			row.append(p)
			if p in default_parameters.keys():
				row.append(default_parameters[p])
				self.agent_parameters[p] = default_parameters[p]
			else:
				row.append("")
				self.agent_parameters[p] = ""

			if p in parameters_info.keys():
				row.append(parameters_info[p])
			else:
				row.append("")
			
			values.append(row)
			row = []

		print("\n Name: " + agent_name)
		print(" Info: " + agents["info"])
		print(" How many stages: " + agents["stages"]["how_many"])
		print()
		tt.print(values, header=headers)
		return True

class AgentInteraction(object):
	def __init__(self, config, session):
		self.config = config
		self.s = session
		self.misc = misc.Misc()
		self.agent = agent.Agent(self.config, self.s, self.misc)
		self.task = task.Task(self.config, self.s, self.misc)

	def menu_current_agent_info(self, agent_uid):
		self.agent.info_agent(agent_uid)
		return True

	def menu_current_agent_name(self, agent_uid):
		agent_name = self.agent.get_agent_name(agent_uid)
		return agent_name

	def menu_edit_agent_group(self, agent_uid, argInput):
		L = len(argInput)
		if L >= 2:
			agent_group = argInput[1]
			r = self.agent.edit_agent_group(agent_uid, agent_group)
		else:
			print("[-] Cannot change the agent group: " + agent_uid)
		return r

	def list_task(self, agent_uid):
		tasks = self.task.list_agent_task(agent_uid)
		tasks = json.loads(tasks)
		headers = ["task uid", "created at", "submited", "completed", "cmd"]
		values = []
		row = []
		for k in tasks.keys():
			task_uid = tasks[k]["task_uid"]
			task_created_at = tasks[k]["task_created_at"]
			task_submited = tasks[k]["task_submited"]
			task_completed = tasks[k]["task_completed"]
			cmd = tasks[k]["cmd_request"]
			cmd += " " + tasks[k]["cmd_arg"]

			row.append(task_uid)
			row.append(task_created_at)
			row.append(task_submited)
			row.append(task_completed)
			row.append(cmd)
			
			values.append(row)
			row = []

		tt.print(values, header=headers)
		return True

	def submit_task(self, agent_uid, argInput):
		cmd_request = argInput[0].upper()
		cmd_arg = ""
		for c in argInput[1:]:
			cmd_arg += c + " "

		cmd_arg = cmd_arg[:-1] # remove the last " "

		task_uid = self.task.create_task(agent_uid, cmd_request, cmd_arg)
		print("[+] Task created: " + task_uid)

		def start_thread(func, name=None, args = []):
			threading.Thread(target=func, name=name, args=args).start()

		def blop(agent_uid, task_uid):
			r = False
			how_many_tries = 100
			while not r:
				time.sleep(2)
				r = self.task.get_result(agent_uid, task_uid)
				how_many_tries -= 1
				if how_many_tries == 0:
					print("[-] Couldn't retrieve the result. Maybe there is an issue on the agent/listener side that couldn't populates the database")
					print("[-] Or the connection to mjollnir_api is not working")
					print("[!] Anyway, you could still use (a few moment later): task -r " + task_uid + " to retrieve the result if the agent is still up")
					break
			return True

		start_thread(blop, args=[agent_uid, task_uid])
		
		return True


class Listener(object):
	def __init__(self, config, session):
		self.config = config
		self.s = session
		self.misc = misc.Misc()
		self.listener_parameters = {}
		self.listener = listener.Listener(self.config, self.s, self.misc)

	def menu_listener_list(self):
		listeners = self.config["listener"]
		listeners_details= listeners["details"]
		listener_details_keys = listeners_details.keys()
		headers = ["name", "type", "info", "used with agent"]
		values = []
		row = []
		for k in listener_details_keys:
			row.append(k)
			row.append(listeners_details[k]["type"])
			row.append(listeners_details[k]["info"])
			row.append(listeners_details[k]["used_with_agents"])
			values.append(row)
			row = []
		
		tt.print(values, header=headers)
		return True
	
	def menu_listener_info(self, listener_name):
		try:
			listeners = self.config["listener"]["details"][listener_name]
		except Exception as e:
			#print(str(e))
			print("[-] This listener does not exist: " + listener_name)
			return False

		parameters = listeners["parameters"]
		parameters_info = listeners["parameters_info"]
		headers = ["PARAMETERS", "VALUES", "INFOS"]
		#headers = parameters
		values = []
		row = []
		#print(self.listener_parameters)
		#print(parameters_info)
		for k in self.listener_parameters.keys():
			row.append(k)
			row.append(self.listener_parameters[k])

			if k in parameters_info.keys():
				row.append(parameters_info[k])
			else:
				row.append("")
			
			values.append(row)
			row = []

		print("\n Name: " + listener_name)
		print(" Info: " + listeners["info"])
		print(" Used with agents: " + listeners["used_with_agents"])
		print()
		tt.print(values, header=headers)

		return True

	def menu_listener_set(self, listener_name, param_value):
		# param_value = (param, value) = (IP, 127.0.0.1)
		try:
			listeners = self.config["listener"]["details"][listener_name]
		except Exception as e:
			#print(str(e))
			print("[-] This listener does not exist: " + listener_name)
			return False

		param = param_value[0]
		if param.upper() in listeners["parameters"]:
			self.listener_parameters[param.upper()] = param_value[1]
		else:
			return False

		return True

	def menu_listener_start(self, listener_name):
		try:
			listeners = self.config["listener"]["details"][listener_name]
		except Exception as e:
			#print(str(e))
			print("[-] This listener does not exist: " + listener_name)
			return False

		for k in self.listener_parameters.keys():
			if self.listener_parameters[k] == "":
				print("[-] You must fill all the required parameters")
				return False


		param_to_send = {}
		for k in self.listener_parameters.keys():
			param_to_send[k] = self.listener_parameters[k]

		param_to_send["listener_name"] = listener_name

		self.listener.create_listener(listener_name, param_to_send)

		return True

	def menu_listener_use(self, listener_name):
		self.listener_parameters = {}
		# retrieve all the listeners name to verify that the name entered by the user exists
		try:
			listeners = self.config["listener"]["details"][listener_name]
		except Exception as e:
			#print(str(e))
			print("[-] This listener does not exist: " + listener_name)
			return False

		# retrieve parameters needed for the selected listener
		parameters = listeners["parameters"]
		default_parameters = listeners["default_parameters"]
		parameters_info = listeners["parameters_info"]
		headers = ["PARAMETERS", "VALUES", "INFOS"]
		values = []
		row = []
		for p in parameters:
			row.append(p)
			if p in default_parameters.keys():
				row.append(default_parameters[p])
				self.listener_parameters[p] = default_parameters[p]
			else:
				row.append("")
				self.listener_parameters[p] = ""

			if p in parameters_info.keys():
				row.append(parameters_info[p])
			else:
				row.append("")
			
			values.append(row)
			row = []

		print("\n Name: " + listener_name)
		print(" Info: " + listeners["info"])
		print(" Used with agents: " + listeners["used_with_agents"])
		print()
		tt.print(values, header=headers)
		return True

class OnRegisteringTask(object):
	def __init__(self, config, session):
		self.config = config
		self.s = session
		self.misc = misc.Misc()
		self.task = task.OnRegisteringTask(self.config, self.s, self.misc)

	def registering_task_list(self, agent_name):
		tasks = self.task.list_registering_tasks_for_agent(agent_name)
		tasks = json.loads(tasks)
		headers = ["task uid", "created at", "cmd"]
		values = []
		row = []
		for k in tasks.keys():
			task_uid = tasks[k]["task_uid"]
			task_created_at = tasks[k]["task_created_at"]
			cmd = tasks[k]["cmd_request"]
			cmd += " " + tasks[k]["cmd_arg"]

			row.append(task_uid)
			row.append(task_created_at)
			row.append(cmd)
			
			values.append(row)
			row = []

		tt.print(values, header=headers)
		return True

		return True

	def registering_task_create(self, agent_name, argInput):
		cmd_request = argInput[0]
		cmd_arg = ""
		for c in argInput[1:]:
			cmd_arg += c + " "
		
		cmd_arg = cmd_arg[:-1] # remove the last " "

		task_uid = self.task.create_registering_task(agent_name, cmd_request, cmd_arg)
		return True

	def registering_task_delete(self, argInput):
		L = len(argInput)
		if L >= 2:
			task_uids = []
			for i in range(1,L):
				task_uids.append(argInput[i])
			self.task.delete_registering_task(task_uids)
		return True

class GroupTask(object):
	def __init__(self, config, session):
		self.config = config
		self.s = session
		self.misc = misc.Misc()
		self.task = task.Task(self.config, self.s, self.misc)
	
	def group_task_list(self, group_name):
		return True

	def group_task_create(self, group_name, argInput):
		cmd_request = argInput[0]
		cmd_arg = ""
		for c in argInput[1:]:
			cmd_arg += c + " "
		cmd_arg = cmd_arg[:-1] # remove the last " "

		task_uid = self.task.create_group_task(agent_name, cmd_request, cmd_arg)
		return True

	def group_task_delete(self, argInput):
		return True

class Mission(object):
	def __init__(self, config, session):
		self.config = config
		self.s = session
		self.misc = misc.Misc()		

class Launcher(object):
	def __init__(self, config, session):
		self.config = config
		self.s = session
		self.misc = misc.Misc()




