from flask import Flask, render_template, request, url_for, flash, redirect
from forms import FormRegister, FormLogin
import json
import datetime
app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = '24293eea8e681f56845df519bac0a473'

# test comment to see if i can push to git repo -stan
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
    # TEST - This allows for basic registration validation, not complex.
    if form.validate_on_submit():
        flash(f'Account created for {form.user.data}!')
        return redirect(url_for('home'))
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
