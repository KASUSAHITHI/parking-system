from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="parking"
)

# 🔐 LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            session["user"] = username
            return redirect("/dashboard")
        else:
            return "Invalid Login"

    return render_template("login.html")


# 🏠 DASHBOARD
@app.route("/dashboard")
def dashboard():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Parking_Slots")
    data = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM Parking_Slots WHERE status='Available'")
    available = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Parking_Slots WHERE status='Occupied'")
    occupied = cursor.fetchone()[0]

    return render_template("dashboard.html", slots=data, available=available, occupied=occupied)


# ➕ ADD SLOT
@app.route("/add", methods=["POST"])
def add():
    slot = request.form["slot"]
    cursor = db.cursor()
    cursor.execute("INSERT INTO Parking_Slots(slot_number, status) VALUES (%s, 'Available')", (slot,))
    db.commit()
    return redirect("/dashboard")


# 🔁 BOOK
@app.route("/book/<int:id>")
def book(id):
    cursor = db.cursor()
    cursor.execute("UPDATE Parking_Slots SET status='Occupied' WHERE slot_id=%s", (id,))
    db.commit()
    return redirect("/dashboard")


# 🔁 UNBOOK
@app.route("/unbook/<int:id>")
def unbook(id):
    cursor = db.cursor()
    cursor.execute("UPDATE Parking_Slots SET status='Available' WHERE slot_id=%s", (id,))
    db.commit()
    return redirect("/dashboard")

print(app.url_map)

app.run(host="0.0.0.0", port=10000)
