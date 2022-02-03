# task.py

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
import json
from . import db, config, decrypt, encrypt
from .models import Task
from .models import OnRegisteringTask
import uuid
from datetime import datetime

task = Blueprint('task', __name__)

# create task
@task.route(config["hidden_route"] + config["endpoints"]["task"] + "/<path:agent_uid>", methods=['POST'])
@login_required
def create_task(agent_uid):  
    try:
        content = request.data
        d = decrypt(content)
    except Exception as e:
        print("[-] Error in create_task()")
        print(str(e))
        return encrypt("[-] Cannot decrypt the request")
    
    d = json.loads(d)

    task_uid = str(uuid.uuid4())

    today = datetime.now()
    task_created_at = today.strftime("%d/%m/%Y - %H:%M")   
    task_submited = False
    task_completed = False
    cmd_request = d["cmd_request"]
    cmd_arg = d["cmd_arg"]
    cmd_result = ""
    #print(cmd_request)
    #print(cmd_arg)

    new_task = Task(task_uid=task_uid, agent_uid=agent_uid, task_created_at=task_created_at, task_submited=task_submited, task_completed=task_completed, cmd_request=cmd_request, cmd_arg=cmd_arg, cmd_result=cmd_result)
    try:
        db.session.add(new_task)
        db.session.commit()
    except Exception as e:
            print("[-] Error in create_task()")
            print("[-] Cannot create a new task")
            print(str(e))
            return encrypt("[-] Cannot create the task: " + task_uid + " for the agent: " + agent_uid)
        
    print("[*] Task created: " + task_uid + " for agent: " + agent_uid)

    return encrypt(task_uid)

# create on registering task
@task.route(config["hidden_route"] + config["endpoints"]["registering_task"] + "/<path:agent_name>", methods=['POST'])
@login_required
def create_registering_task(agent_name):  
    try:
        content = request.data
        d = decrypt(content)
    except Exception as e:
        print("[-] Error in create_registering_task()")
        print(str(e))
        return encrypt("[-] Cannot decrypt the request")
    
    d = json.loads(d)

    task_uid = str(uuid.uuid4())
    today = datetime.now()
    task_created_at = today.strftime("%d/%m/%Y - %H:%M")   
    cmd_request = d["cmd_request"]
    cmd_arg = d["cmd_arg"]

    new_task = OnRegisteringTask(task_uid=task_uid, task_created_at=task_created_at, agent_name=agent_name, cmd_request=cmd_request, cmd_arg=cmd_arg)
    try:
        db.session.add(new_task)
        db.session.commit()
    except Exception as e:
            print("[-] Error in create_registering_task()")
            print("[-] Cannot create a new 'on registering task'")
            print(str(e))
            return encrypt("[-] Cannot create the 'on registering task': " + task_uid + " for the agent_name: " + agent_name)
        
    print("[*] On registering task created: " + task_uid + " for agent name: " + agent_name)

    return encrypt(task_uid)

# get task result
@task.route(config["hidden_route"] + config["endpoints"]["task"] + "/<path:task_uid>", methods=['GET'])
@login_required
def get_task_result(task_uid):
    task = Task.query.filter_by(task_uid=task_uid).first()

    r = {}

    if task:
        if task.task_completed:
            r[task_uid] = [True, task.cmd_result, task.cmd_request, task.cmd_arg]
        else: # the task is not completed
            if not task.task_completed:
                r[task_uid] = [False, "", task.cmd_request, task.cmd_arg]
    else:
        r[task_uid] = [False, "", "", ""]

    r = json.dumps(r)

    return encrypt(r)

# list tasks for agent_uid
@task.route(config["hidden_route"] + config["endpoints"]["task"], methods=['GET'])
@login_required
def list_agent_tasks():
    agent_uid = request.args.get("agent_uid")
    tasks = Task.query.filter_by(agent_uid=agent_uid).all()

    r = {}

    for task in tasks:
        tmp = {}
        tmp["task_uid"] = task.task_uid
        tmp["task_created_at"] = task.task_created_at
        tmp["task_submited"] = task.task_submited
        tmp["task_completed"] = task.task_completed
        tmp["cmd_request"] = task.cmd_request
        if len(task.cmd_arg) > 80:
            tmp["cmd_arg"] = task.cmd_arg[0:80] + " ..."
        else:
            tmp["cmd_arg"] = task.cmd_arg
        
        r[task.task_uid] = tmp

    r = json.dumps(r)

    return encrypt(r)


# delete all tasks for an  agent
@task.route(config["hidden_route"] + config["endpoints"]["task"], methods=['DELETE'])
@login_required
def delete_all_tasks():
    try:
        content = request.data
        agent_uid = decrypt(content)
    except Exception as e:
        print("[-] Error in delete_all_tasks()")
        print(str(e))
        return encrypt("[-] Cannot decrypt the request")

    tasks = Task.query.filter_by(agent_uid = agent_uid)

    for task in tasks:
        try:
            db.session.delete(task)
            db.session.commit()
        except Exception as e:
            print("[-] Error in delete_agent()")
            print("[-] Cannot delete the agent")
            print(str(e))
            return encrypt("[-] Cannot delete the task: " + task.task_uid + " for the agent: " + task.agent_uid)
    

    return encrypt("[+] All tasks deleted for the agent: " + agent_uid)

"""
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
"""