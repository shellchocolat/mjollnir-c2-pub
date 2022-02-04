# __init__.py
 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import json
from base64 import b64decode, b64encode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import uuid
import os

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

#import os
current_dir = os.getcwd()
with open("./config.json", "r") as fp:
    config = fp.read()
config = json.loads(config)

def create_app():
    app = Flask(__name__, 
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

    app.config['SECRET_KEY'] = 'ddLWGND4om3j4K3i4op1'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mjollnir-c2.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_uid):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(user_uid)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    from .mission import mission as mission_blueprint
    app.register_blueprint(mission_blueprint)

    from .listener import listener as listener_blueprint
    app.register_blueprint(listener_blueprint)

    from .agent import agent as agent_blueprint
    app.register_blueprint(agent_blueprint)

    from .task import task as task_blueprint
    app.register_blueprint(task_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

def decrypt(cipher):
    # echo "aG73s7ppN7eyHGPEfzOpLqCiHaM7wIv2p9l5IHI4jr6LMRLoSFzkxwIdfc8RN/EzUgkOr07/mGU4xujRZZoxM8mRmD6WVesSL4QCqjQlwcOC5sOjp6yBLzxE3jjWbptSexCOof52ZKo6vfwd8g095wsUP0pbhH5zcunAkNKIaInwn6+v8BeRjcMlEwg2KKrXt2/kHwgubAc+pIvgymNT/3KLj6/8tLboLPk9jArtj8/gqut0YO+U7Elr58sTyKQFY/vHdrVh1UiyY+pg0FwX7FhcC+d9vB05MchMXQAg+9h7mGMUq5vQpx7HErpLYGKByqBfICpfr8mFaDWqB1N75lT7xZBmOkSNwCOXPvF7lks5hMjVvdhBuKqHD+O9esfLI2e4PBynFRL8XexjpHzgI0+JjhD+BtYSJrRPdvigBamSJrW3zV0QcQEYYxOXynM7IpTKTHSo0bZZhJWWtmGokZaa7nPnZMVq85TAtJ4zyEN9C0PB6ngbmW5HOY4yH2PwTN8Aprwn9S0fjGhu6gbUF7bIuovFIBBQ0ecOH20w0oabIRhPJvEnSND0PIcIrXxekjUt7pxptY5kfuY/+cmcYvSGSt/0Laf0GW6pM1KONfn/fbhlqrKB6G0+PnYmYsaeREC3NfuXRi16rTwJxD1Rewtd53KjXirKuP2xl9TCleQ=" | base64 -d | openssl rsautl -decrypt -inkey /home/shellchocolat/mjollnir-c2_v2/mjollnir-api/certificates/authent-rsa.priv
    """
    plain = None
    cipher = b64decode(cipher)
    try:
        with open(config["crypto"]["private_key_path"], "rb") as k:
            key = RSA.importKey(k.read())

        decipher = PKCS1_v1_5.new(key)
        plain = decipher.decrypt(cipher, None).decode()
    except Exception as e:
        print("[-] Error in decrypt()")
        print(e)
    
    #print("DECRYPTION: " + str(plain))
    return plain
    """
    return b64decode(cipher).decode()

def encrypt(plain):
    # echo "test" | openssl rsautl -encrypt -pubin -inkey /home/shellchocolat/mjollnir-c2_v2/mjollnir-api/certificates/authent-rsa.pub | base64
    """
    cipher = None
    try:
        with open(config["crypto"]["public_key_path"], "rb") as k:
            key = RSA.importKey(k.read())

        c = PKCS1_v1_5.new(key)
        cipher = c.encrypt(plain.encode())
    except Exception as e:
        print("[-] Error in encrypt()")
        print(e)

    cipher = b64encode(cipher)

    #print("ENCRYPTION: " + str(cipher))
    return cipher
    """
    return b64encode(plain.encode())
