import json
import misc
import termtables as tt

class Listener():
	def __init__(self, config, session, misc):
		self.config = config
		self.s = session
		self.misc = misc

	def delete_listener(self, listeners_uid):
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["listener"]
		for listener_uid in listeners_uid:
			data = self.misc.encrypt(listener_uid)
			r = self.s.delete(url+endpoint, data=data)
			if r.status_code == 200:
				print(self.misc.decrypt(r.content))
			else:
				print("[-] Cannot delete listener: " + listener_uid)
		return True

	def create_listener(self, listener_name, listener_param):
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["listener"]

		data = listener_param
		data["listener_name"] = listener_name
		data = json.dumps(data)

		data = self.misc.encrypt(data)
		r = self.s.post(url+endpoint, data=data)
		if r.status_code == 200:
			print(self.misc.decrypt(r.content))
			return True
		else:
			print("[-] Cannot start the listener")
			return False


	def list_listeners(self):
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["listeners"]
		r = self.s.get(url+endpoint)
		if r.status_code == 200:
			try:
				j = json.loads(self.misc.decrypt(r.content))
				#print(j)
				headers = ["uid", "type", "listener_name", "bind address", "bind port", "status", "pid"]
				values = []
				for k in j.keys():
					row = j[k]
					values.append(row)
					
				tt.print(values, header=headers)
			except Exception as e:
				print(str(e))
				print(self.misc.decrypt(r.content))
		else:
			print("[-] Cannot list listeners")
			return False
		return True