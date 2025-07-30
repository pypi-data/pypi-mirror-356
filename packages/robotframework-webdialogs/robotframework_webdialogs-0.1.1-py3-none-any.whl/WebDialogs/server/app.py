from flask import Flask, render_template

from .blueprints.api import api
from .blueprints.dialog import dialog

app = Flask(__name__)

app.register_blueprint(api)
app.register_blueprint(dialog)


@app.route("/")
def home():
    return render_template("home.html")
