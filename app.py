from flask import Flask, render_template, request, redirect, session
import sqlite3
import joblib

app = Flask(__name__)
app.secret_key = "secret123"

# 🔥 LOAD MODEL
model = joblib.load("model.pkl")

# 🔗 DB CONNECT
def connect_db():
    return sqlite3.connect("database.db")

# 💊 FERTILIZER LOGIC
def get_fertilizer(crop):
    crop = crop.lower()

    if crop == "rice":
        return "Urea + DAP"
    elif crop == "wheat":
        return "NPK + Urea"
    elif crop == "maize":
        return "Compost + NPK"
    else:
        return "Organic Fertilizer"

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("login.html")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        user = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = connect_db()
        conn.execute("INSERT INTO users(username,email,password) VALUES(?,?,?)",
                     (user,email,password))
        conn.commit()
        conn.close()

        return redirect("/")
    return render_template("register.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    conn = connect_db()
    user = conn.execute("SELECT * FROM users WHERE email=? AND password=?",
                        (email,password)).fetchone()
    conn.close()

    if user:
        session["user"] = user[1]
        return redirect("/dashboard")
    else:
        return "❌ Invalid Login"

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html")

# ---------------- PREDICTION ----------------
@app.route("/predict", methods=["GET","POST"])
def predict():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        N = float(request.form["N"])
        P = float(request.form["P"])
        K = float(request.form["K"])
        temp = float(request.form["temp"])
        humidity = float(request.form["humidity"])
        ph = float(request.form["ph"])
        rainfall = float(request.form["rainfall"])

        # 🌱 ML Prediction
        crop = model.predict([[N,P,K,temp,humidity,ph,rainfall]])[0]

        # 💊 Fertilizer
        fertilizer = get_fertilizer(crop)

        # 💾 SAVE HISTORY
        conn = connect_db()
        conn.execute(
            "INSERT INTO history(user, crop, fertilizer) VALUES (?,?,?)",
            (session["user"], crop, fertilizer)
        )
        conn.commit()
        conn.close()

        return render_template("result.html", crop=crop, fertilizer=fertilizer)

    return render_template("predict.html")

# ---------------- HISTORY ----------------
@app.route("/history")
def history():
    if "user" not in session:
        return redirect("/")

    conn = connect_db()
    data = conn.execute(
        "SELECT crop, fertilizer, date FROM history WHERE user=?",
        (session["user"],)
    ).fetchall()
    conn.close()

    return render_template("history.html", data=data)

# ---------------- WEATHER ----------------
@app.route("/weather")
def weather():
    if "user" not in session:
        return redirect("/")
    return render_template("weather.html")

# ---------------- GRAPH ----------------
@app.route("/graph")
def graph():
    if "user" not in session:
        return redirect("/")
    return render_template("graph.html")

# ---------------- NEWS ----------------
@app.route("/news")
def news():
    if "user" not in session:
        return redirect("/")
    return render_template("news.html")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)