from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
db = SQLAlchemy()
db.init_app(app)

class cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    map_url = db.Column(db.String, unique=False, nullable=False)
    img_url = db.Column(db.String, unique=False, nullable=False)
    location = db.Column(db.String, unique=False, nullable=False)
    has_sockets = db.Column(db.BOOLEAN, unique=False, nullable=False)
    has_toilet = db.Column(db.BOOLEAN, unique=False, nullable=False)
    has_wifi = db.Column(db.BOOLEAN, unique=False, nullable=False)
    can_take_calls = db.Column(db.BOOLEAN, unique=False, nullable=False)
    seats = db.Column(db.VARCHAR, unique=False, nullable=False)
    coffee_price = db.Column(db.VARCHAR, unique=False, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    locations = db.session.execute(db.select(cafe))
    a = locations.scalars().all()
    for loc in a:
        print(loc.name)
    return render_template("index.html", locations=a)

if __name__ == "__main__":
    app.run(debug=True)