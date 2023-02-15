from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("secret_key")
    app.config["MYSQL_USER"] = "root"
    app.config["MYSQL_PASSWORD"] = os.environ.get("mysql_pass")
    app.config["MYSQL_DB"] = "lookmoney"

    return app
