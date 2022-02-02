import json
import misc
import termtables as tt

class Mission():
	def __init__(self, config, session, misc):
		self.config = config
		self.s = session
		self.misc = misc

	def list_missions(self):
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["missions"]
		r = self.s.get(url+endpoint)
		if r.status_code == 200:
			try:
				j = json.loads(self.misc.decrypt(r.content))
				#print(j)
				headers = ["uid", "name"]
				values = []
				for k in j.keys():
					row = j[k]
					values.append(row)
				tt.print(values, header=headers)
			except Exception as e:
				print(str(e))
				print(self.misc.decrypt(r.content))
		else:
			print("[-] Cannot list missions")
			return False
		return True

	def create_mission(self, mission_name):
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["mission"]
		data = self.misc.encrypt(mission_name)
		r = self.s.post(url+endpoint, data=data)
		if r.status_code == 200:
			print(self.misc.decrypt(r.content))
		else:
			print("[-] Cannot create the mission: " + mission_name)
			return False
		return True

	def delete_mission(self, missions_uid):
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["mission"]
		for mission_uid in missions_uid:
			data = self.misc.encrypt(mission_uid)
			r = self.s.delete(url+endpoint, data=data)
			if r.status_code == 200:
				print(self.misc.decrypt(r.content))
			else:
				print("[-] Cannot delete the mission: " + mission_uid)
		return True


	def select_mission(self, mission_uid):
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["mission"]
		headers = {
					self.config["headers"]["mission_uid"]: self.misc.encrypt(mission_uid)
				}
		r = self.s.get(url+endpoint, headers=headers)
		if r.status_code == 200:
			d = self.misc.decrypt(r.content)
			if d == "1": # mission exist
				print("[+] Mission selected")
			else: # mission does not exist
				print("[-] Mission not selected - not exist?")
		else:
			print("[-] Cannot select the mission: " + mission_uid)
			return False
		return True