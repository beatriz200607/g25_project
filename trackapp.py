from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'

def get_fake_location(seed_value):
    random.seed(int(seed_value))
    lat = 38.736946 + random.uniform(-0.01, 0.01)
    lng = -9.142685 + random.uniform(-0.01, 0.01)
    return lat, lng

@app.route("/", methods=["GET", "POST"])
def index():
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

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
