from flask import Flask
from flask import render_template, url_for, redirect, request, flash, session
from flask_login import LoginManager
from forms import RegistrationFormPacient, AddRequestFormular, RegistrationFormDoctor, LoginFormDoctor
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from models import Doctor, db, Pacient, Requests
from datetime import datetime


app = Flask(__name__)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    user_role = session.get('user_role') 
    
    if user_role == 'Doctor':
        return Doctor.query.get(int(user_id))
    elif user_role == 'Pacient':
        return Pacient.query.get(int(user_id))
    
    return None  


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zochovamed.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.secret_key = 'kluckluckluc'


def datetimeformat(value, format="%Y-%m-%d %H:%M:%S"):
    return datetime.fromisoformat(value).strftime(format)

app.jinja_env.filters["datetimeformat"] = datetimeformat


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about_us.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        flash(f'Thank you {name}, we have received your message!', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')



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
        flash('Registration successful', 'success')
        return redirect(url_for('home'))

    return render_template('registerdoctor.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginFormDoctor()
    if form.validate_on_submit():
        userdoctor = Doctor.query.filter_by(email=form.email.data).first()
        userpatient = Pacient.query.filter_by(email=form.email.data).first()
        
        if userdoctor and userdoctor.check_password(form.password.data):
            login_user(userdoctor)
            session['user_role'] = 'Doctor'  
            flash('Logged in as doctor', 'success')
            return redirect(url_for('home'))
        
        elif userpatient and userpatient.check_password(form.password.data):
            login_user(userpatient)
            session['user_role'] = 'Pacient'  
            flash('Logged in as patient', 'success')
            return redirect(url_for('home'))
        
        else:
            flash('Incorrect email or password', 'error')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)





@app.route('/explorepacient')
@login_required
def explorepacient():
    doc = Doctor.query.all()
    return render_template('explorepacient.html', doctors=doc)

@app.route('/viewdoctor/<int:id>', methods=['GET', 'POST'])
@login_required
def viewdoctor(id):
    doctorprofile = Doctor.query.get_or_404(id)
    form = AddRequestFormular()
    if form.validate_on_submit():

        new_request = Requests(description=form.problem_desc.data, time_sent=datetime.today().isoformat(), to_id=id, from_id=current_user.id)
        db.session.add(new_request)
        db.session.commit()
        flash('Request sent successfully', 'success')
        return redirect(url_for('home'))

    return render_template('viewdoctor.html', doctorprofile=doctorprofile, form=form)

@app.route('/findpatients')
@login_required
def findpatients():
    if session.get('user_role') != 'Doctor':  # Use session role for security
        flash("Access denied. Patients cannot view this page.", "error")
        return redirect(url_for('home'))
    
    requests = Requests.query.filter_by(to_id=current_user.id).all()
    return render_template('findpatients.html', requests=requests)


@app.route('/view_request/<int:request_id>')
@login_required
def view_request(request_id):
    request_data = Requests.query.get_or_404(request_id)
    pacient_data = Pacient.query.get(request_data.from_id)
    return render_template('viewrequest.html', request=request_data, pacient=pacient_data)


with app.app_context():
    db.create_all()