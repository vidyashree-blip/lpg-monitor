import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = "lpg_secret_key_2026"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lpgweb.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# --- Database Models ---
class User(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(100))
    email     = db.Column(db.String(100), unique=True)
    password  = db.Column(db.String(200))
    device_id = db.Column(db.String(50))

class Reading(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(50))
    timestamp = db.Column(db.String(100))
    ppm       = db.Column(db.Float)
    weight_kg = db.Column(db.Float)
    status    = db.Column(db.String(20))

# --- Routes ---
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name      = request.form["name"]
        email     = request.form["email"]
        password  = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")
        device_id = request.form["device_id"]

        existing = User.query.filter_by(email=email).first()
        if existing:
            return render_template("signup.html", error="Email already registered!")

        user = User(name=name, email=email, password=password, device_id=device_id)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email    = request.form["email"]
        password = request.form["password"]
        user     = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session["user_id"]   = user.id
            session["user_name"] = user.name
            session["device_id"] = user.device_id
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Wrong email or password!")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    device_id = session["device_id"]

    # Get latest real reading from database
    latest = Reading.query.filter_by(device_id="ESP32-001")

    if latest:
        ppm       = latest.ppm
        weight_kg = latest.weight_kg
        status    = latest.status
    else:
        # Simulate if no real data yet
        ppm       = random.randint(100, 1200)
        weight_kg = round(random.uniform(2.0, 14.2), 2)
        if ppm >= 1000:
            status = "DANGER"
        elif ppm >= 500:
            status = "WARNING"
        else:
            status = "SAFE"

        reading = Reading(
            device_id = device_id,
            timestamp = datetime.now().strftime("%d %b %Y %I:%M %p"),
            ppm       = ppm,
            weight_kg = weight_kg,
            status    = status
        )
        db.session.add(reading)
        db.session.commit()

    percent = round((weight_kg / 14.2) * 100)

    alerts = Reading.query.filter_by(device_id=device_id)\
             .order_by(Reading.id.desc()).limit(5).all()

    return render_template("dashboard.html",
        name      = session["user_name"],
        ppm       = ppm,
        weight_kg = weight_kg,
        percent   = percent,
        status    = status,
        alerts    = alerts
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/api/sensor-data", methods=["POST"])
def receive_sensor_data():
    from leak_detector import detect_leak

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400

    ppm       = float(data.get("ppm", 0))
    weight_kg = float(data.get("weight_kg", 0))

    result = detect_leak(ppm)

    reading = Reading(
        device_id = "ESP32-001",
        timestamp = datetime.now().strftime("%d %b %Y %I:%M %p"),
        ppm       = ppm,
        weight_kg = weight_kg,
        status    = result["status"]
    )
    db.session.add(reading)
    db.session.commit()

    return jsonify({
        "status": "ok",
        "ppm"       : ppm,
        "weight_kg" : weight_kg,
        "alert"     : result["status"]
    }), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Website database ready.")
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)