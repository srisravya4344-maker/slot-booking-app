from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Booking

app = Flask(__name__)
app.secret_key = "slotbooking123"

# Railway MySQL Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:QmfXCfFPNaSlQWrBeNVKYfcrQGYwfNQS@kodama.proxy.rlwy.net:55146/railway"
)

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "connect_args": {
        "ssl": {}
    }
}

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize Database
db.init_app(app)

# Create tables automatically
with app.app_context():
    db.create_all()

# Available Slots
SLOTS = [
    "09:00 AM",
    "10:00 AM",
    "11:00 AM",
    "12:00 PM",
    "01:00 PM",
    "02:00 PM",
    "03:00 PM",
    "04:00 PM",
]

# Home Page
@app.route("/")
def index():
    booked_slots = [booking.slot_time for booking in Booking.query.all()]
    available_slots = [slot for slot in SLOTS if slot not in booked_slots]

    return render_template(
        "index.html",
        slots=available_slots
    )

# Book Slot
@app.route("/book/<slot>", methods=["GET", "POST"])
def book(slot):

    if request.method == "POST":

        existing = Booking.query.filter_by(slot_time=slot).first()

        if existing:
            flash("This slot is already booked!", "danger")
            return redirect(url_for("index"))

        booking = Booking(
            name=request.form["name"],
            email=request.form["email"],
            phone=request.form["phone"],
            slot_time=slot
        )

        db.session.add(booking)
        db.session.commit()

        flash("Slot booked successfully!", "success")

        return redirect(url_for("bookings"))

    return render_template("book.html", slot=slot)

# View Bookings
@app.route("/bookings")
def bookings():

    all_bookings = Booking.query.order_by(Booking.booking_date.desc()).all()

    return render_template(
        "bookings.html",
        bookings=all_bookings
    )

if __name__ == "__main__":
    app.run(debug=True)