from flask import Flask, render_template, request, session
import random

from classes.dish import Dish
from datafile import filename
from classes.order import Order
from classes.restaurant import Restaurant
from classes.deliverypartner import DeliveryPartner
from classes.userlogin import Userlogin

from subs.apps_gform import apps_gform 
from subs.apps_subform import apps_subform 
from subs.apps_userlogin import apps_userlogin

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'

# Load initial data
Order.read(filename + 'Trabalho.db')
Restaurant.read(filename + 'Trabalho.db')
Dish.read(filename + 'Trabalho.db')
DeliveryPartner.read(filename + 'Trabalho.db')
Userlogin.read(filename + 'business.db')

# Utility: generate fake location based on ID
def get_fake_location(seed_value):
    random.seed(int(seed_value))
    lat = 38.736946 + random.uniform(-0.01, 0.01)
    lng = -9.142685 + random.uniform(-0.01, 0.01)
    return lat, lng

# Routes
@app.route("/")
def index():
    return render_template("index.html", ulogin=session.get("user"))

@app.route("/login")
def login():
    return render_template("login.html", user="", password="", ulogin=session.get("user"), resul="")

@app.route("/logoff")
def logoff():
    session.pop("user", None)
    return render_template("index.html", ulogin=session.get("user"))

@app.route("/chklogin", methods=["POST", "GET"])
def chklogin():
    user = request.form["user"]
    password = request.form["password"]
    resul = Userlogin.chk_password(user, password)
    if resul == "Valid":
        session["user"] = user
        return render_template("index.html", ulogin=session.get("user"))
    return render_template("login.html", user=user, password=password, ulogin=session.get("user"), resul=resul)

@app.route("/gform/<cname>", methods=["POST", "GET"])
def gform(cname):
    return apps_gform(cname)

@app.route("/subform/<cname>", methods=["POST", "GET"])
def subform(cname):
    return apps_subform(cname)

@app.route("/Userlogin", methods=["POST", "GET"])
def userlogin():
    return apps_userlogin()

# New tracking route
@app.route("/track", methods=["GET", "POST"])
def track():
    lat = lng = None
    track_type = track_id = ""

    option = request.args.get("option")
    if request.method == "POST":
        option = "track"

    if option == "track":
        track_type = request.form.get("track_type")
        track_id = request.form.get("track_id")
        if track_id and track_id.isdigit():
            lat, lng = get_fake_location(track_id)

    elif option == "exit":
        return "<h1>Obrigado por usar esta aplicação!</h1>"

    return render_template("index_track.html",
                           track_id=track_id,
                           track_type=track_type,
                           lat=lat,
                           lng=lng,
                           ulogin=session.get("user"))

# Run
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
