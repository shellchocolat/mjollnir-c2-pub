from .models import User
from . import db, config, decrypt, encrypt
from flask_login import login_user, logout_user, login_required
from flask import Blueprint, request
import uuid
import hashlib

auth= Blueprint('auth', __name__)

@auth.route(config["hidden_route"] + config["endpoints"]["login"], methods=['POST'])
def login():
    user_name = request.form.get('username')
    password = request.form.get('password')
    md5_hash = hashlib.md5(password.encode()).hexdigest()
    user = User.query.filter_by(user_name=user_name).first()

    if not user:
        return encrypt("[-] error login()")
    else:
        if md5_hash != user.user_hash:
            return encrypt("[-] error login()")

    # if the above check passes, then we know the user has the right credentials
    login_user(user)
    return encrypt("[+] Login successful: " + user.user_uid)

@auth.route(config["hidden_route"] + config["endpoints"]["logout"])
@login_required
def logout():
    logout_user()
    return encrypt("[+] Logout successful")

@auth.route(config["hidden_route"] + config["endpoints"]["first_user"], methods=['POST'])
def first_user():
    # create first user
    user_name = request.form.get('username')
    password = request.form.get('password')
    user_hash = hashlib.md5(password.encode()).hexdigest()
    user_role = "admin"
    user_uid = str(uuid.uuid4())

    user = User.query.filter_by(user_name=user_name).first()

    if user:
        return encrypt("[-] first_user() cannot be used anymore")

    first_user = User(user_uid=user_uid, user_name=user_name, user_role=user_role, user_hash=user_hash)
    db.session.add(first_user)
    db.session.commit()

    return encrypt("[+] First user created: " + user_uid)
