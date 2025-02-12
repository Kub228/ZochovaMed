from flask import Flask
from flask import render_template, url_for, redirect, request, flash
from flask_login import LoginManager
#from forms import PridajClanokFormular
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
#from forms import RegistrationForm, LoginForm
#from models import Clanok, db, User
from flask_migrate import Migrate

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')