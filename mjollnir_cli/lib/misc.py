
from base64 import b64encode, b64decode

class Misc():
	def __init__(self):
		pass

	def decrypt(self, cipher):
		try:
			r = b64decode(cipher).decode()
		except:
			r = cipher
		return r
	
	def encrypt(self, plain):
		try:
			r = b64encode(plain.encode())
		except:
			r = plain
		return r

	def mission_selected(mission_name):
		if mission_name != "":
			return True
		else:
			return False
