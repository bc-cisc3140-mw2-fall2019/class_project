from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy  import SQLAlchemy # pip install Flask-SQLAlchemy https://www.youtube.com/watch?v=Tu4vRU4lt6k
from flask_bootstrap import Bootstrap # pip install flask-bootstrap
from forms import FormRegister, FormLogin
import json
import datetime
app = Flask(__name__, template_folder="templates")
Bootstrap (app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://testuser:test123@127.0.0.1:3306/testdatabase'#setup a connection mysql://username:password@localhost/database https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/#connection-uri-format not sure why "+pymysql" is needed but without it, it didnt let me connect. cant find where i found the fix
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #removes warnings 

app.config['SECRET_KEY'] = '24293eea8e681f56845df519bac0a473'

db = SQLAlchemy(app) #set db var


# to comment block of code use CTRL + K and CTRL + C one after the other and to uncomment use CTRL + k and CTRL + U to uncomment a block of highlighted code

class registerUser(db.Model): #create our database https://www.youtube.com/watch?v=cYWiDiIUxQc different video
    __tablename__ = 'user login' #name of our database table
    id = db.Column(db.Integer, primary_key = True, autoincrement=True) # have id assigned to each user with autoincrementing numbers
    email = db.Column(db.String(50), unique = True, nullable= False) #have a username setup to a String type max of 15 characters, have the String be unique, and make sure that the field cant be left empty which is nullable= false
    username = db.Column(db.String(15), unique = True, nullable= False) #username column with string type and holding max of 15 chars, its unique so no duplicates are registered
    password = db.Column(db.String(30), unique = False, nullable= False)# password is also a column doesnt have to be unique but cant be left empty

date = datetime.datetime.now()
fakeData = [
    {
        'ID': '23290',
        'dateCreated': date
    },
    {
        'ID': '23291',
        'dateCreated': date
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', info=fakeData)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = FormRegister()
   # commented out code to see if the page still runs without any errors and still sends data to database (it does)
    # TEST - This allows for basic registration validation, not complex.
    # if form.validate_on_submit():
    #     flash(f'Account created for {form.user.data}!')
    #     return redirect(url_for('home'))

#------------------------------------------ not exactly sure why this is needed but itll throw me errors without the if seen it at https://stackoverflow.com/questions/42579079/flask-post-data-to-table-using-sqlalchemy-mysql
    if request.method == 'GET':
        return render_template('register.html',form=form)
#----------------------------------------------------------------
   # autoincrement = 0 #need to figure out how to auto increment id's so no duplicate id is created and no error is thrown
    registration = registerUser( email=request.form.get('email'),username=request.form.get('user'), password = request.form.get('password')) # registration variable that will hold our registration class registerUser(id, email, user, password) each field is a column in our MySQL database
    
    db.session.add(registration) #we capture the session into our database 
    db.session.commit() #and after we capture the session we commit it into the database
    #endtest
    return render_template('register.html', form=form) 


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = FormLogin()
    # TEST - Allowing this user+pass combo - Change with DB incorporation.
    if form.validate_on_submit():
        if form.user.data == 'admin1' and form.password.data == 'password':
            flash(f'Successful Login! Welcome {form.user.data}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Unsuccessful Login', 'danger')
    #endtest
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
