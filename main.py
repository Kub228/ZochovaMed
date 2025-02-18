from flask import Flask
from flask import render_template, url_for, redirect, request, flash
from flask_login import LoginManager
from forms import RegistrationFormPacient, AddRequestFormular, RegistrationFormDoctor, LoginForm
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from models import Doctor, db, Pacient, Requests
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zochovamed.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.secret_key = 'kluckluckluc'

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/registerpacient', methods=['GET', 'POST'])
def registerpacient():
    form = RegistrationFormPacient()
    if form.validate_on_submit():
        pacient = Pacient.query.filter_by(email=form.email.data).first()
        if pacient:
            return redirect(url_for('registerpacient'))

        new_pacient = Pacient(first_name=form.firstname.data, last_name=form.lastname.data, tel_num = form.telnum.data, description=form.description.data , email=form.email.data)
        new_pacient.set_password(form.password.data)
        db.session.add(new_pacient)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('registerpacient.html', form=form)

@app.route('/registerdoctor', methods=['GET', 'POST'])
def registerdoctor():
    form = RegistrationFormDoctor()
    if form.validate_on_submit():
        doctor = Doctor.query.filter_by(email=form.email.data).first()
        if doctor:
            return redirect(url_for('registerdoctor'))

        new_doctor = Doctor(first_name=form.firstname.data, last_name=form.lastname.data, tel_num = form.telnum.data, odbor=form.odbor.data , email=form.email.data)
        new_doctor.set_password(form.password.data)
        db.session.add(new_doctor)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('registerdoctor.html', form=form)



with app.app_context():
    db.create_all()