import os
import json
from datetime import datetime
from flask import Flask, render_template, request, url_for, flash, redirect, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from forms import FormRegister, FormLogin, ResetPasswordForm, PostForm, UpdateBio
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_mail import Mail, Message
app = Flask(__name__, template_folder="templates")

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@127.0.0.1:3306/dbname'#setup a connection mysql://username:password@localhost/database https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/#connection-uri-format not sure why "+pymysql" is needed but without it, it didnt let me connect. cant find where i found the fix
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
#     username="users",
#     password="password",
#     hostname="127.0.0.1:3306",
#     databasename="database name",
# )

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

# app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# set configuration and instantiate mail

mail_settings = {
    "MAIL_SERVER": 'smtp.googlemail.com',
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": True,
    "MAIL_USE_SSL": False,
    "MAIL_USERNAME": os.environ.get('EMAIL_USER'),
    "MAIL_PASSWORD": os.getenv('EMAIL_PASS')
}

# The following two must be set as environment variables
# app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
# app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
app.config.update(mail_settings)
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
    __tablename__ = 'users_tb' # Name of our database table
    id = db.Column(db.Integer, primary_key = True, autoincrement = True) 
    fname = db.Column(db.String(20), nullable = False)
    lname = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False)
    username = db.Column(db.String(15), unique = True, nullable = False) 
    password = db.Column(db.String(50), unique = False, nullable = False)
    occupation = db.Column(db.String(100))
    bio = db.Column(db.String(100))
    github_link = db.Column(db.String(100))
    posts = db.relationship('Posts', backref='author', lazy=True)
    

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


# Post class has 5 fields:
# post_id: unique ID associated with every post
# title: String for a post title
# content: String for a post content
# id: Foreign key for the User table. Every post has a foreign key to its author (ID)
class Posts(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users_tb.id'), nullable=False)

    # def __repr__(self):
    #     return f"Post('{self.title}', '{self.date_posted}')"


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


# 3 fields for updating an account
# user field requires valid data (must be unique)
# email field requires valid data (must be unique)
# submit is a field for submission
class UpdateAccForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update Account')

    # Validation for username: Must not be taken by another account username
    def validate_username(self, username):
        if username.data != current_user.username:
            user = registerUser.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    #Validation for email: Must not be taken by another account email
    def validate_email(self, email):
        if email.data != current_user.email:
            user = registerUser.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
 
        


@app.route('/')
@app.route('/home')
def home():
    # Query every post to the front page, sorted by newest post
    posts = Posts.query.all()
    posts.reverse()
    return render_template('index.html', posts=posts)


@app.route('/home/old')
def old():
    posts = Posts.query.all()
    return render_template('old.html', posts=posts)


@app.route('/home/best')
def best():
    posts = Posts.query.all()
    posts.sort(key=lambda x: x.likes, reverse=True)
    return render_template('best.html', posts=posts)


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
        
        registration = registerUser(fname=request.form.get('fname'), lname=request.form.get('lname'), email=request.form.get('email'), username=request.form.get('user'), password=hashed_password, occupation="No Occupation", bio="N/A", github_link="N/A")

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


@app.route("/account", methods=['GET', 'POST'])
@login_required #############**IMPORTANT TO UNCOMMENT WHEN DONE TESTING**################
def account():
    form = UpdateAccForm()

    if form.validate_on_submit():
        # If the form is valid, change the current user/email information to the form input information
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        return redirect(url_for('account'))
    elif request.method == 'GET':
        # Otherwise, if the form is invalid, replace any invalid form information with the current user/email information
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html", form=form)


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@app.route("/editProfile", methods=['GET', 'POST'])
@login_required ####### ********IMPORTNAT********** TO UNCOMMENT WHEN DONE TESTING remove login required to work on the page without logging in###################################
def editProfile():
    form = UpdateBio()

    if form.validate_on_submit():
        current_user.occupation = form.occupation.data
        current_user.bio = form.bio.data
        current_user.github_link = form.github_link.data
        db.session.commit()

        return redirect(url_for('editProfile'))
    elif request.method == 'GET':
        # Otherwise, if the form is invalid, replace any invalid form information with the current user/email information
        form.occupation.data = current_user.occupation
        form.bio.data = current_user.bio
        form.github_link.data = current_user.github_link
    return render_template("editProfile.html", form=form)

@app.route("/newProjects")
def newProject():
    return render_template("newProject.html")

@app.route("/about")
def aboutPage():
    return render_template("about.html")


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
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))

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


# Route for creating a new post.
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def newPost():
    # Create an instance of the PostForm class
    form = PostForm()
    if form.validate_on_submit():
        # Create a row in the Post table with the information provided in the form
        post = Posts(title=form.title.data,
                     content=form.content.data, author=current_user, likes=1)

        # Add the row to the database, commit the addition, and redirect to home page with the new post
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('newPost.html', form=form)


# Route for a specific post (not currently functioning for some reason)
@app.route("/post/<int:post_id>")
def post(post_id):
    # Query for the post with the unique ID if it exists
    post = Posts.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/profile/specificProject")
def specificProject():
    return render_template('specificProject.html')


@app.route("/upvote", methods=['POST'])
@login_required
def upvote():
    if request.method == "POST":
        data_received = json.loads(request.data)
        print(data_received)
        post = Posts.query.filter_by(post_id=data_received['postid']).first()

        if post:
            setattr(post, "likes", post.likes + 1)
            db.session.commit()

            return json.dumps({'status': 'success'})
        return json.dumps({'status': 'no post found'})
    return redirect(url_for('index'))


# ----------------------------------------------------------
#
# Error handling:
# 404: If the page doesn't exist
# 403: If the user has no permission to perform an action
# 500: Internal error on the server end
# Errors for handling 403, 404, and 500
errors = Blueprint('errors', __name__)


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500


app.register_blueprint(errors)

# ----------------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True)
