from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo

class AddRequestFormular(FlaskForm):
    problem_desc = TextAreaField('Describe your problem', validators=[DataRequired()])
    send = SubmitField('SEND')


class RegistrationFormPacient(FlaskForm):
    firstname = StringField('Your first name', validators=[DataRequired()])
    lastname = StringField('Your last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telnum = StringField('Your phone number', validators=[DataRequired()])
    description = TextAreaField('Something about yourself', validators=[DataRequired()])
    #este pridat datum narodenia
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class RegistrationFormDoctor(FlaskForm):
    firstname = StringField('Your first name', validators=[DataRequired()])
    lastname = StringField('Your last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telnum = StringField('Your phone number', validators=[DataRequired()])
    #este pridat datum narodenia
    odbor = StringField('Your field', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Heslo', validators=[DataRequired()])
    submit = SubmitField('Prihlásiť sa')