import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Booking

app = Flask(__name__)
app.secret_key = "slotbooking123"

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Railway may provide mysql:// instead of mysql+pymysql://
    if DATABASE_URL.startswith("mysql://"):
        DATABASE_URL = DATABASE_URL.replace(
            "mysql://", "mysql+pymysql://", 1
        )
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql://root:QmfXCfFPNaSlQWrBeNVKYfcrQGYwfNQS@kodama.proxy.rlwy.net:55146/railway"
    )

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "connect_args": {
        "ssl": {}
    }
}

db.init_app(app)

with app.app_context():
    db.create_all()

SLOTS = [
    "09:00 AM",
    "10:00 AM",
    "11:00 AM",
    "12:00 PM",
    "01:00 PM",
    "02:00 PM",
    "03:00 PM",
    "04:00 PM"
]


@app.route("/")
def index():
    booked_slots = [b.slot_time for b in Booking.query.all()]
    available_slots = [slot for slot in SLOTS if slot not in booked_slots]
    return render_template("index.html", slots=available_slots)


@app.route("/book/<slot>", methods=["GET", "POST"])
def book(slot):

    if request.method == "POST":

        existing = Booking.query.filter_by(slot_time=slot).first()

        if existing:
            flash("This slot is already booked!", "warning")
            return redirect(url_for("index"))

        booking = Booking(
            name=request.form["name"],
            email=request.form["email"],
            phone=request.form["phone"],
            slot_time=slot,
        )

        db.session.add(booking)
        db.session.commit()

        flash("Slot booked successfully!", "success")
        return redirect(url_for("bookings"))

    return render_template("book.html", slot=slot)


@app.route("/bookings")
def bookings():
    bookings = Booking.query.order_by(Booking.booking_date.desc()).all()
    return render_template("bookings.html", bookings=bookings)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))