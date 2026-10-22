from sqlalchemy import Integer, String, Boolean, inspect
from flask import Flask, render_template, request, url_for, redirect, flash, abort
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
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
csrf = CSRFProtect(app)
bootstrap = Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "admin_login"

class Admin(UserMixin):
    id = "admin"


@login_manager.user_loader
def load_user(user_id):
    if user_id == "admin":
        return Admin()
    return None

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

class CafeSuggestion(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)
    status: Mapped[str] = mapped_column(String(25), nullable=False, default="pending")

with app.app_context():
    db.create_all()

    inspector = inspect(db.engine)

    print("Database file:", db.engine.url.database)
    print("Physical tables:", inspector.get_table_names())



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

class AdminLoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

@app.route('/')
def home():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()

    return render_template("index.html", all_cafes=all_cafes)

@app.route('/suggestions', methods=['GET', 'POST'])
def suggestions():
    form = AddSuggestion()
    if form.validate_on_submit():
        new_cafe = CafeSuggestion(
        name = form.name.data,
        map_url = form.map_url.data,
        img_url = form.img_url.data,
        location = form.location.data,
        seats = form.seats.data,
        has_toilet = True if form.has_toilet.data == "True" else False,
        has_wifi = True if form.has_wifi.data == "True" else False,
        has_sockets = True if form.has_sockets.data == "True" else False,
        can_take_calls = True if form.can_take_calls.data == "True" else False,
        coffee_price = form.coffee_price.data or None,
        )

        db.session.add(new_cafe)
        db.session.commit()

        flash("Your suggestion was submitted for review!")
        return redirect(url_for('home'))
    return render_template("suggest.html", form=form)

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    form = AdminLoginForm()

    if form.validate_on_submit():
        username = os.environ.get("ADMIN_USERNAME")
        password = os.environ.get("ADMIN_PASSWORD")

        if form.username.data == username and form.password.data == password:
            admin = Admin()
            login_user(admin)
            return redirect(url_for("admin_dashboard"))

        flash("Invalid username or password.")

    return render_template("login.html", form=form)

@app.route("/admin")
@login_required
def admin_dashboard():
    result = db.session.execute(
        db.select(CafeSuggestion).where(CafeSuggestion.status == "pending")
    )
    pending_suggestions = result.scalars().all()

    return render_template(
        "admin.html",
        suggestions=pending_suggestions
    )

@app.route("/admin/approve/<int:suggestion_id>", methods=["POST"])
@login_required
def approve_suggestion(suggestion_id):
    suggestion = db.get_or_404(CafeSuggestion, suggestion_id)

    if suggestion.status != "pending":
        abort(400)

    new_cafe = Cafe(
        name=suggestion.name,
        map_url=suggestion.map_url,
        img_url=suggestion.img_url,
        location=suggestion.location,
        seats=suggestion.seats,
        has_toilet=suggestion.has_toilet,
        has_wifi=suggestion.has_wifi,
        has_sockets=suggestion.has_sockets,
        can_take_calls=suggestion.can_take_calls,
        coffee_price=suggestion.coffee_price,
    )

    db.session.add(new_cafe)
    suggestion.status = "approved"
    db.session.commit()

    flash(f"{suggestion.name} was approved successfully!")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/reject/<int:suggestion_id>", methods=["POST"])
@login_required
def reject_suggestion(suggestion_id):
    suggestion = db.get_or_404(CafeSuggestion, suggestion_id)

    if suggestion.status != "pending":
        abort(400)

    suggestion.status = "rejected"
    db.session.commit()

    flash(f"{suggestion.name} was rejected.")
    return redirect(url_for("admin_dashboard"))

if __name__ == "__main__":
    app.run(debug=True)