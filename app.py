import os, sys
from flask import Flask, render_template, request, redirect

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)

from pymongo import MongoClient

_col = None
def get_col():
    global _col
    if _col is None:
        uri = os.environ.get("MONGO_URI", "")
        if not uri:
            raise RuntimeError("MONGO_URI not set")
        _col = MongoClient(uri, serverSelectionTimeoutMS=5000)["edutrack"]["students"]
    return _col

@app.route("/")
def home():
    try:
        students = list(get_col().find({}, {"_id": 0}))
    except Exception:
        students = []
    return render_template("index.html", students=students)

@app.route("/add", methods=["POST"])
def add():
    try:
        get_col().insert_one({
            "name": request.form.get("name"),
            "email": request.form.get("email")
        })
    except Exception:
        pass
    return redirect("/")
