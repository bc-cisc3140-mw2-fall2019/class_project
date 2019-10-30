# This is a test registration form using wtforms - you must do: pip install flask-wtf

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
#from app import registerUser #Circular import, folder/file structure must change

class FormRegister(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    user = StringField('Username', validators=[DataRequired(), Length(min=5, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    #--- To fix following, the structure of the folders/files must change, if we want to do it this way ---#

    # Because of circular imports, this won't work. This is a user-duplicate check
    # def validate_user(self, user):
    #     user = registerUser.query.filter_by(user=user.data).first()
    #     if user:
    #         raise ValidationError('Username already taken')

    # This won't work either. Email duplicate check
    # def validate_email(self, email):
    #     user = registerUser.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValidationError('Email already taken')


class FormLogin(FlaskForm):
    user = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
