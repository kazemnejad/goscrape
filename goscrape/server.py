# -*- coding: utf8 -*-
from sqlalchemy import or_

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

from ai import get_suggested_apps
from goscrape.database import config
from goscrape.database.models import Application

app = Flask(__name__)
app.debug = True
app.secret_key = config.SECRET_KEY

CORS(app)


@app.route("/suggest", methods=["POST"])
def suggest():
    component_names = request.form.getlist("appid[]")

    conditions = []
    for cn in component_names:
        conditions.append(Application.component_name == cn)

    suggested = get_suggested_apps([app for app in Application.query.filter(or_(*conditions))])

    return render_template("suggest.html", apps=suggested)


@app.route("/search/app/<string:query>", methods=["GET"])
def search(query):
    if len(query) < 2:
        return jsonify({"items": []})

    words = query.split(u" ")
    conditions = []
    for word in words:
        conditions.append(Application.name.like("%" + word + "%"))

    result = Application.query.filter(or_(*conditions))
    found_apps = []
    for appl in result:
        found_apps.append({
            "name": appl.name,
            "component": appl.component_name,
            "icon": appl.icon,
            "url": "https://cafebazaar.ir/app/" + appl.component_name,
            "category": appl.categories[0].name,
            "price": appl.price,
            "rate": appl.rate,
            "developer": appl.developer.name
        })

    return jsonify({"items": found_apps})


@app.route("/")
def index():
    return render_template("homepage.html")


def run():
    global app
    app.run(threaded=True)
