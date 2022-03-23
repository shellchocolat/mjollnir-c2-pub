# models.py

from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    user_uid = db.Column(db.String(100), unique=True)
    user_name = db.Column(db.String(100), unique=True)
    user_hash = db.Column(db.String(100))
    user_role = db.Column(db.String(100))

class Mission(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    mission_uid = db.Column(db.String(100), unique=True)
    mission_name = db.Column(db.String(100))
    #user_uid = db.Column(db.String(100))

class Listener(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    listener_uid = db.Column(db.String(100), unique=True)
    listener_name = db.Column(db.String(100))
    listener_type = db.Column(db.String(100))
    listener_bind_address = db.Column(db.String(100))
    listener_bind_port = db.Column(db.String(100))
    listener_status = db.Column(db.String(32))
    listener_pid = db.Column(db.String(8))

class Agent(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    agent_uid = db.Column(db.String(100), unique=True)
    agent_name = db.Column(db.String(100))
    agent_group = db.Column(db.String(100))
    agent_type = db.Column(db.String(100))
    agent_os = db.Column(db.String(100))
    agent_created_at = db.Column(db.String(100))
    agent_activated = db.Column(db.String(100))
    agent_last_check = db.Column(db.String(100))
    agent_ip_address = db.Column(db.String(100))
    agent_hostname = db.Column(db.String(100))
    agent_username = db.Column(db.String(100))
    agent_integrity_level = db.Column(db.String(100))
    agent_version = db.Column(db.String(100))

class Shellcode(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    shellcode_uid = db.Column(db.String(100), unique=True)
    shellcode_name = db.Column(db.String(100))
    shellcode_type = db.Column(db.String(100))
    shellcode_os = db.Column(db.String(100))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    task_uid = db.Column(db.String(100))
    agent_uid = db.Column(db.String(100))
    task_created_at = db.Column(db.String(100))
    task_submited = db.Column(db.Boolean)
    task_completed = db.Column(db.Boolean)
    cmd_request = db.Column(db.String(100))
    cmd_arg = db.Column(db.String(100000))
    cmd_result = db.Column(db.String(100000))
    
class OnRegisteringTask(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    task_uid = db.Column(db.String(100))
    task_created_at = db.Column(db.String(100))
    agent_name = db.Column(db.String(100))
    cmd_request = db.Column(db.String(100))
    cmd_arg = db.Column(db.String(100000))
    