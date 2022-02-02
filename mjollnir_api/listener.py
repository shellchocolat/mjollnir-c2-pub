# listener.py

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
import json
from . import db, config, decrypt, encrypt
from .models import Listener
import uuid
import subprocess
import shlex
import time
import os, signal


listener = Blueprint('listener', __name__)

# create a listener
@listener.route(config["hidden_route"] + config["endpoints"]["listener"], methods=['POST'])
@login_required
def create_listener():
    try:
        content = request.data
        d = decrypt(content)
    except Exception as e:
        print("[-] Error in create_listener()")
        print(str(e))
        return encrypt("[-] Cannot decrypt the request")

    d = json.loads(d)
    #print(d)
    
    listener_uid = str(uuid.uuid4())
    listener_name = d["listener_name"]
    listener_path = config["listener"]["details"][listener_name]["path"]
    params = config["listener"]["details"][listener_name]["parameters"]
    listener_bind_address = d["IP"]
    listener_bind_port = d["PORT"]
    listener_status = "started"
    listener_type = config["listener"]["details"][listener_name]["type"]

    listeners = Listener.query.filter_by(listener_bind_port=listener_bind_port).first()

    if listeners: # mean that a listener is already started
        return encrypt("[-] Listener already started: " + listeners.listener_uid)

    try:
        c = listener_path + " " + listener_bind_address + " " + listener_bind_port

        cc = shlex.split(c)
        process = subprocess.Popen(cc, start_new_session=True)
        print("starting listener " + listener_uid + " ...")
        time.sleep(2)
        pid = process.pid

    except Exception as e:
        print(str(e))
        pid = 0

    if pid != 0:
        new_listener = Listener(listener_uid=listener_uid, listener_type=listener_type, listener_name=listener_name, listener_bind_address=listener_bind_address, listener_bind_port=listener_bind_port, listener_status=listener_status, listener_pid=pid)
        try:
            db.session.add(new_listener)
            db.session.commit()
        except Exception as e:
            print("[-] Error in create_listener()")
            print("[-] Cannot create a new listener")
            print(str(e))
            return encrypt("[-] Cannot create the listener")
    else:
        return encrypt("[-] Cannot create the listener")

    return encrypt("[+] Listener created: " + listener_uid)


# delete a listener
@listener.route(config["hidden_route"] + config["endpoints"]["listener"], methods=['DELETE'])
@login_required
def delete_listener():
    try:
        content = request.data
        d = decrypt(content)
    except Exception as e:
        print("[-] Error in delete_listener()")
        print(str(e))
        return encrypt("[-] Cannot decrypt the request")

    listener = Listener.query.filter_by(listener_uid = d).first()

    try:
        os.kill(int(listener.listener_pid), signal.SIGKILL)
    except Exception as e:
        print("[-] Error in delete_listener()")
        print("[-] Cannot delete the listener")
        print(str(e))

    db.session.delete(listener)
    db.session.commit()

    return encrypt("[+] Listener deleted: " + d)


# list all listeners
@listener.route(config["hidden_route"] + config["endpoints"]["listeners"], methods=['GET'])
@login_required
def list_listeners():
    listeners = Listener.query.all()
    r = {}
    tmp = []

    for l in listeners:
        #print(l.id)
        #print(l.listener_uid)
        #print(l.listener_type)
        tmp.append(l.listener_uid)
        tmp.append(l.listener_type)
        tmp.append(l.listener_name)
        tmp.append(l.listener_bind_address)
        tmp.append(l.listener_bind_port)
        tmp.append(l.listener_status)
        tmp.append(l.listener_pid)

        r[l.listener_uid] = tmp
        tmp = []

    r = json.dumps(r) # to convert json to string
    print(r)
    return encrypt(r)
