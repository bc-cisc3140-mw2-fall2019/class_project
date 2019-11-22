import os
from flask import Flask, render_template, request, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from forms import FormRegister, FormLogin, ResetPasswordForm
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_mail import Mail, Message
app = Flask(__name__, template_folder="templates")

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@127.0.0.1:3306/dbName'#setup a connection mysql://username:password@localhost/database https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/#connection-uri-format not sure why "+pymysql" is needed but without it, it didnt let me connect. cant find where i found the fix
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
     username="user",
     password="password",
     hostname="127.0.0.1:3306",
    databasename="dbName",
)

# Note: in order to not store passwords in the file, you must set up environment variables for:
# 1) database URI 
# 2) secret key
# 3) an actual email username (in this case it's using gmail)
# 4) that email username's password
# 
# TO SET UP AN ENVIRONMENT VARIABLE: https://www.youtube.com/watch?v=IolxqkL7cD8

# Use this format for DATABASE_URI environment variable: 'mysql+pymysql://user:password@127.0.0.1:3306/dbName'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('C_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #removes warnings 

# For example, set environment variable to: 24293eea8e681f56845df519bac0a473 Link to set up EV: https://www.youtube.com/watch?v=IolxqkL7cD8
app.config['SECRET_KEY'] = 'any secret string'# random key could be anything you set it to (reccommended to random generate key but for us its okay to put whatever) i.e app.config['SECRET_KEY'] = 'put whatever key you want here'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # Flask didn't see the updates in JS and CSS files, that because by default, Flask has as max-age value 12 hours. You can set it to 0 to resolve the problem
# For example, set the following environment variable to: 24293eea8e681f56845df519bac0a473


db = SQLAlchemy(app) #set db var
bcrypt = Bcrypt(app) #set encrypt variable
login_manager = LoginManager(app)
login_manager.login_view = 'login'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

# The following two must be set as environment variables
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)


# This method handles a user being logged in. Finds the user associated with the given ID and logs the individual in.
@login_manager.user_loader
def load_user(user_id):
    return registerUser.query.get(int(user_id))


# An instance of the registerUser has 7 fields:
# the database table name used (for local db)
# ID: A unique number associated with each user
# First name and last name
# A unique email (valid), username, and password
class registerUser(db.Model, UserMixin): #create our database https://www.youtube.com/watch?v=cYWiDiIUxQc different video
    __tablename__ = 'user_login' # Name of our database table
    id = db.Column(db.Integer, primary_key = True, autoincrement = True) 
    fname = db.Column(db.String(20), nullable = False)
    lname = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False)
    username = db.Column(db.String(15), unique = True, nullable = False) 
    password = db.Column(db.String(30), unique = False, nullable = False)

    # Uses secret key to generate a token that lasts for 30 minutes (used for password reset)
    def getToken(self, expires_seconds=1800):
        serial = Serializer(app.config['SECRET_KEY'], expires_seconds)
        return serial.dumps({'user_id': self.id}).decode('utf-8')

    # Accepts a token, creates a serializer, and then loads the token
    @staticmethod
    def verifyToken(token):
        serial = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = serial.loads(token)['user_id']
        except:
            return None
        return registerUser.query.get(user_id)


# 3 fields for password reset, used for sending a reset email link
# email field requires valid data
# confirmEmail field must be equal to email
# submit is a field for submission
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    confirmEmail = StringField('ConfirmEmail', validators=[DataRequired(), Email(), EqualTo('email')])
    submit = SubmitField('Request Password Reset')

    # Accepts reference to current instance and an email, and will check if that email exists in the database
    def validateEmail(self, email):
        user = registerUser.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = FormRegister()
    #----------------------- not exactly sure why this is needed but itll throw me errors without the if seen it at https://stackoverflow.com/questions/42579079/flask-post-data-to-table-using-sqlalchemy-mysql
    if request.method == 'GET':
        return render_template('register.html',form=form)
    #-----------------------

    # If the form is valid, create a hashed + salted password and store all the user information in the database.
    # The data includes: first name, last name, email, username, and the hashed+salted password.
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        registration = registerUser(fname=request.form.get('fname'), lname=request.form.get('lname'), email=request.form.get('email'), username=request.form.get('user'), password=hashed_password)

        db.session.add(registration)  
        db.session.commit()  
        
        flash(f'Account created for {form.user.data}!')
        return redirect(url_for('login'))

    return render_template('register.html', form=form) 


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # Create instance of FormLogin
    form = FormLogin()

    # If the form is valid, find the user using input data. 
    if form.validate_on_submit():
        user = registerUser.query.filter_by(username=form.user.data).first()
    
        # If the password matches the password associated with that user in the database, login the user.
        # Otherwise, return and prompt 'unsuccessful login.'
        if (user and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Unsuccessful Login', 'danger')
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template("account.html")


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@app.route("/editProfile")
#@login_required ####### ********IMPORTNAT********** TO UNCOMMENT WHEN DONE TESTING remove login required to work on the page without logging in###################################
def editProfile():
    return render_template("editProfile.html")

@app.route("/newProjects")
def newPRoject():
    return render_template("newProject.html")



# Accepts a user and sends an email using flask-mail
def sendResetEmail(user):
    token = user.getToken()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link: 
    {url_for('resetPassword', token=token, _external=True)}
    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)


# User must not be logged in to access this route. 
# Takes input for email, retrieves the user ID with that email from the database, and sends an email.
@app.route("/forgotPassword", methods=['GET', 'POST'])
def forgotPassword():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RequestResetForm()

    # If valid, first occurence of user ID with that email.
    if form.validate_on_submit():
        user = registerUser.query.filter_by(email=form.email.data).first()
        sendResetEmail(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))

    return render_template("forgotPassword.html", form=form)


# Reset Password route based on email sent (URL includes token). This template needs a token to be accessed
@app.route("/resetPassword/<token>", methods=['GET', 'POST'])
def resetPassword(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    user = registerUser.verifyToken(token)
    
    # If the token doesn't exist or expired, return and take no action. Otherwise, continue on.
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('forgotPassword'))
    
    # Create instance of ResetPasswordForm
    form = ResetPasswordForm()
    
    # If the instance is valid, create a hashed+salted password using input and set that as the user's new password
    # Save new changes to database
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    
    return render_template('resetPassword.html', title='Reset Password', form=form)


if __name__ == '__main__':
    app.run(debug=True)
