# user.py

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
import json
from . import db, config, decrypt, encrypt
from .models import User
import uuid
from datetime import datetime

user = Blueprint('user', __name__)

# list all users
@user.route(config["hidden_route"] + config["endpoints"]["users"], methods=['GET'])
@login_required
def list_users():
    users = User.query.all()
    r = {}
    tmp = []

    for u in users:
        tmp.append(u.user_uid)
        tmp.append(u.user_name)
        tmp.append(u.user_role)

        r[u.user_uid] = tmp
        tmp = []

    r = json.dumps(r) # to convert json to string
    return encrypt(r)
