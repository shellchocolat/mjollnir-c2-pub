# shellcode.py

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
import json
from . import db, config, decrypt, encrypt, current_dir
from .models import Shellcode
import time
import subprocess
import shlex
import binascii

shellcode = Blueprint('shellcode', __name__)

def get_shellcode_bytes(filename):
    try:
        with open(filename, 'rb') as fp:
            hexdata = binascii.hexlify(fp.read())
        r = str(hexdata.decode())
        return r
    except Exception as e:
        print(str(e))
        print("[-] Cannot open " + filename)
        return "[-] Cannot open the shellcode: " + filename


# create shellcode - generate - compile
@shellcode.route(config["hidden_route"] + config["endpoints"]["shellcode"], methods=['POST'])
@login_required
def generate_shellcode():
    try:
        content = request.data
        d = decrypt(content)
    except Exception as e:
        print("[-] Error in generate_shellcode()")
        print(str(e))
        return encrypt("[-] Cannot decrypt the request")

    d = json.loads(d)

    shellcode_name = d["shellcode_name"]
    shellcode_builder = current_dir + config["shellcode"]["details"][shellcode_name]["builder"]
    params = config["shellcode"]["details"][shellcode_name]["parameters"]
    source_code = current_dir + config["shellcode"]["details"][shellcode_name]["source_code"]
    c = shellcode_builder
    for p in params:
        c += " " + d[p]
    c += " " + source_code + " " + shellcode_name
    #print("#######################")
    #print(c)
        
    cc = shlex.split(c)
    subprocess.Popen(cc, start_new_session=True)

    time.sleep(2)

    r = "[+] Shellcode generated: " + shellcode_name + "\n\n"
    r+= get_shellcode_bytes("/home/shellchocolat/mjollnir-c2-pub/mjollnir_shellcodes/windows/x64/a.bin")
    r+= "\n"
    #print(r)
    return encrypt(r)

