from flask import Flask, render_template, request, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy # pip install Flask-SQLAlchemy https://www.youtube.com/watch?v=Tu4vRU4lt6k
from flask_bcrypt import Bcrypt
from forms import FormRegister, FormLogin
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
app = Flask(__name__, template_folder="templates")

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@127.0.0.1:3306/dbName'#setup a connection mysql://username:password@localhost/database https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/#connection-uri-format not sure why "+pymysql" is needed but without it, it didnt let me connect. cant find where i found the fix
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="user",
    password="password",
    hostname="127.0.0.1:3306",
    databasename="dbName",
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #removes warnings 
app.config['SECRET_KEY'] = '24293eea8e681f56845df519bac0a473'

db = SQLAlchemy(app) #set db var
bcrypt = Bcrypt(app) #set encrypt variable
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return registerUser.query.get(int(user_id))

# to comment block of code use CTRL + K and CTRL + C one after the other and to uncomment use CTRL + k and CTRL + U to uncomment a block of highlighted code

class registerUser(db.Model, UserMixin): #create our database https://www.youtube.com/watch?v=cYWiDiIUxQc different video
    __tablename__ = 'user_login' #name of our database table
    id = db.Column(db.Integer, primary_key = True, autoincrement = True) # have id assigned to each user with autoincrementing numbers
    fname = db.Column(db.String(20), nullable = False)
    lname = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False) #have a username setup to a String type max of 15 characters, have the String be unique, and make sure that the field cant be left empty which is nullable= false
    username = db.Column(db.String(15), unique = True, nullable = False) #username column with string type and holding max of 15 chars, its unique so no duplicates are registered
    password = db.Column(db.String(30), unique = False, nullable = False)# password is also a column doesnt have to be unique but cant be left empty


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = FormRegister()
#------------------------------------------ not exactly sure why this is needed but itll throw me errors without the if seen it at https://stackoverflow.com/questions/42579079/flask-post-data-to-table-using-sqlalchemy-mysql
    if request.method == 'GET':
        return render_template('register.html',form=form)
#------------------------------------------
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        registration = registerUser(fname=request.form.get('fname'), lname=request.form.get('lname'), email=request.form.get('email'), username=request.form.get('user'), password=hashed_password)  # registration variable that will hold our registration class registerUser(id, email, user, password) each field is a column in our MySQL database

        db.session.add(registration)  # we capture the session into our database
        db.session.commit()  # and after we capture the session we commit it into the database
        
        flash(f'Account created for {form.user.data}!')
        return redirect(url_for('login'))

    return render_template('register.html', form=form) 


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = FormLogin()
    if form.validate_on_submit():
        user = registerUser.query.filter_by(username=form.user.data).first()
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


@app.route("/projects")
@login_required
def projects():
    return render_template("projects.html")


if __name__ == '__main__':
    app.run(debug=True)
