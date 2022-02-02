import json
import misc
import termtables as tt
import getpass

class User():
	def __init__(self, config, session, misc):
		self.config = config
		self.s = session
		self.misc = misc

	def first_user(self, username, password):
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["first_user"]
		data = {
				"username": username,
				"password": password
			}
		r = self.s.post(url+endpoint, data=data)
		if r.status_code == 200:
			print(self.misc.decrypt(r.content))
		else:
			print("[-] Cannot create the first user")

	def user_logout(self):
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["logout"]
		r = self.s.get(url+endpoint)
		if r.status_code == 200:
			print(self.misc.decrypt(r.content))
		else:
			print("[-] Cannot logout")
		return True

	def user_login(self, argInput):
		L = len(argInput)
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["login"]
		if L == 1:
			username = input("username: ")
			password = getpass.getpass(prompt='password: ')
		elif L == 2:
			username = argInput[1]
			password = getpass.getpass(prompt='password: ')
		else:
			username = argInput[1]
			password = argInput[2]

		data = {
				"username": username,
				"password": password
		}
		r = self.s.post(url+endpoint, data=data)
		if r.status_code == 200:
			print(self.misc.decrypt(r.content))
		else:
			print("[-] Cannot login with: " + username)
			return False
		return True

	def list_users(self):
		url = self.config["mjollnir_c2_url"] + self.config["hidden_route"]
		endpoint = self.config["endpoints"]["users"]
		r = self.s.get(url+endpoint)
		if r.status_code == 200:
			try:
				j = json.loads(self.misc.decrypt(r.content))
				#print(j)
				headers = ["uid", "name", "role"]
				values = []
				for k in j.keys():
					row = j[k]
					values.append(row)
					
				tt.print(values, header=headers)
			except Exception as e:
				print(str(e))
				print(self.misc.decrypt(r.content))
		else:
			print("[-] Cannot list the users")
			return False
		return True
