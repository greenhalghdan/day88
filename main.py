from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import wtforms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, URL
from flask_bootstrap import Bootstrap5

app = Flask(__name__)

app.config['SECRET_KEY'] = 'anotveryrandomstringofletters'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
db = SQLAlchemy()
db.init_app(app)
bootstrap = Bootstrap5(app)

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


class addCafeForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    map_url = StringField("Map URL", validators=[DataRequired(), URL()])
    img_url = StringField("Image URL", validators=[DataRequired(), URL()])
    location = StringField("Location", validators=[DataRequired()])
    has_sockets = SelectField("Power Sockets", choices=[(True, "Yes"), (False, "No")], coerce=bool)
    has_toilet = SelectField("Toilets", choices=[(True, "Yes"), (False, "No")], coerce=bool)
    has_wifi = SelectField("WiFi", choices=[(True, "Yes"), (False, "No")], coerce=bool)
    can_take_calls = SelectField("Phone Calls", choices=[(True, "Yes"), (False, "No")], coerce=bool)
    seats = StringField("Number of Seats", validators=[DataRequired()])
    coffee_price = StringField("Cost of the Coffee", validators=[DataRequired()], default="£")
    submit = SubmitField("Submit Post")

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    locations = db.session.execute(db.select(cafe))
    a = locations.scalars().all()
    for loc in a:
        print(loc.has_toilet)
    return render_template("index.html", locations=a)


@app.route('/add', methods=["GET", "POST"])
def add():
    addcafe = addCafeForm()
    if addcafe.validate_on_submit():
        print(addcafe.data.get("name"))
        db.session.add(cafe(
            name = addcafe.data.get('name'),
            map_url = addcafe.data.get('map_url'),
            img_url = addcafe.data.get('img_url'),
            location = addcafe.data.get('location'),
            has_sockets = bool(addcafe.data.get('has_sockets')),
            has_toilet = bool(addcafe.data.get('has_toilet')),
            has_wifi = bool(addcafe.data.get('has_wifi')),
            can_take_calls = bool(addcafe.data.get('can_take_calls')),
            seats = addcafe.data.get('seats'),
            coffee_price = addcafe.data.get('coffee_price'),
        ))
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("add.html", form=addcafe)

if __name__ == "__main__":
    app.run(debug=True)