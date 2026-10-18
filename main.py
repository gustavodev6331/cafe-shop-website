from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

class Base(DeclarativeBase):
    pass

db_path = os.path.join(os.path.dirname(__file__), "cafes.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

with app.app_context():
    print(db.engine.url)

class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


class AddSuggestion(FlaskForm):
    name = StringField("Coffee name", validators=[DataRequired()])
    map_url = StringField("Coffee map", validators=[DataRequired()])
    img_url = StringField("Coffee picture", validators=[DataRequired()])
    location = StringField("Coffee location", validators=[DataRequired()])
    seats = StringField("Coffee seats", validators=[DataRequired()])
    has_toilet = SelectField(
        "Has a customer toilet?",
        choices=[("True", "Yes"), ("False", "No")],
        validators=[DataRequired()]
    )

    has_wifi = SelectField(
        "Has Wi-Fi?",
        choices=[("True", "Yes"), ("False", "No")],
        validators=[DataRequired()]
    )

    has_sockets = SelectField(
        "Has power outlets?",
        choices=[("True", "Yes"), ("False", "No")],
        validators=[DataRequired()]
    )

    can_take_calls = SelectField(
        "Can customers take calls?",
        choices=[("True", "Yes"), ("False", "No")],
        validators=[DataRequired()]
    )
    coffee_price = StringField("Coffee price (Optional)")
    submit = SubmitField("Add suggestion to be reviewd from website owner")



@app.route('/')
def home():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()

    return render_template("index.html", all_cafes=all_cafes)

@app.route('/suggestions', methods=['GET', 'POST'])
def suggestions():
    form = AddSuggestion()
    if form.validate_on_submit():
        flash("Your suggestion was submitted for review!")
        return redirect(url_for('home'))
    return render_template("suggest.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)