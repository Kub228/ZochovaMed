from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



db = SQLAlchemy()


class Pacient(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=True, nullable=False)
    last_name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    tel_num = db.Column(db.String(120), unique=True, nullable=False) #telefonne cislo
    password_hash = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False) # nieco o pacientovy


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Doctor(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=True, nullable=False)
    last_name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    tel_num = db.Column(db.String(120), unique=True, nullable=False) #telefonne cislo
    password_hash = db.Column(db.String(128), nullable=False)
    #date_birth = db.Column(db.Date, nullable=False)
    odbor = db.Column(db.String(80)) # zameranie doktora (psycholog, chirurg, ...)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

# Trieda pre jednotlive rezervacie pacientov pre doktorov
class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_id = db.Column(db.Integer, nullable=False)#id pacienta
    to_id = db.Column(db.Integer, nullable=False)#id doktora
    description = db.Column(db.Text, nullable=False)#opis problemu pacienta
    time_sent = db.Column(db.String, nullable=False) #kedy bol request poslany



