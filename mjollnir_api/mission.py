# mission.py

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
import json
from . import db, config, decrypt, encrypt, current_dir
from .models import Mission
import uuid


mission = Blueprint('mission', __name__)

# select a mission
@mission.route(config["hidden_route"] + config["endpoints"]["mission"], methods=['GET'])
@login_required
def select_mission():
    # mission name inside a custom header
    try:
        headers = request.headers.get(config["headers"]["mission"])
        d = decrypt(headers)
    except Exception as e:
        print("[-] Error in select_mission()")
        print(str(e))
        return encrypt("[-] Cannot decrypt the request")

    mission = Mission.query.filter_by(mission_uid = d).first()
    if mission:
        return encrypt("1")
    else:
        return encrypt("0")

# create a mission
@mission.route(config["hidden_route"] + config["endpoints"]["mission"], methods=['POST'])
@login_required
def create_mission():
    try:
        content = request.data
        d = decrypt(content)
    except Exception as e:
        print("[-] Error in create_mission()")
        print(str(e))
        return encrypt("[-] Cannot decrypt the request")

    mission_uid = str(uuid.uuid4())
    mission_name = d
    new_mission = Mission(mission_uid=mission_uid, mission_name=mission_name)
    try:
        db.session.add(new_mission)
        db.session.commit()
    except Exception as e:
        print("[-] Error in create_mission()")
        print("[-] Cannot create a new mission")
        print(str(e))
        return encrypt("[-] Cannot create the mission")
    
    return encrypt("[+] Mission created: " + mission_uid)

# update a mission
@mission.route(config["hidden_route"] + config["endpoints"]["mission"], methods=['PUT'])
@login_required
def update_mission():
    return encrypt("hello world")

# delete a mission
@mission.route(config["hidden_route"] + config["endpoints"]["mission"], methods=['DELETE'])
@login_required
def delete_mission():
    try:
        content = request.data
        d = decrypt(content)
    except Exception as e:
        print("[-] Error in delete_mission()")
        print(str(e))
        return encrypt("[-] Cannot decrypt the request")
    
    try:
        mission = Mission.query.filter_by(mission_uid = d).first()
        db.session.delete(mission)
        db.session.commit()
    except Exception as e:
        print("[-] Error in delete_mission()")
        print("[-] Cannot delete the mission")
        print(str(e))
        return encrypt("[-] Cannot delete the mission")
    

    return encrypt("[+] Mission deleted: " + d)


# /MISSIONS
############

# list all missions
@mission.route(config["hidden_route"] + config["endpoints"]["missions"], methods=['GET'])
@login_required
def list_missions():
    missions = Mission.query.all()

    r = {}
    tmp = []
    for m in missions:
        #print(m.id)
        #print(m.mission_uid)
        #print(m.mission_name)
        tmp.append(m.mission_uid)
        tmp.append(m.mission_name)

        r[m.mission_uid] = tmp
        tmp = []

    r = json.dumps(r) # to convert json to string
    return encrypt(r)
