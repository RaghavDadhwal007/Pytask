from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_mysqldb import MySQL
from wtforms import Form, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
from flask_session import Session
from functools import wraps

app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'db'

mysql = MySQL(app)

import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem' 
app.config['SESSION_PERMANENT']= False
sess = Session()
sess.init_app(app)


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    
  

@app.route('/', methods=['POST', 'GET'])
def index():
    try:
        form = RegistrationForm(request.form)
        if request.method == "POST" and form.validate():
            
            username  = form.username.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c =  mysql.connection.cursor()
            x = c.execute("SELECT * FROM users WHERE username = '%s'" % (username))
            
            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)

            else:
                c.execute("INSERT INTO users (username, password) VALUES ('{0}', '{1}')".format((username), (password)))    
                mysql.connection.commit()
                flash("Thanks for registering!")
                c.close()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('login_page'))

        return render_template("register.html", form=form)

    except Exception as e:
        return(str(e))
		

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login_page'))

    return wrap


@app.route('/login/', methods=["GET","POST"])
def login_page():
    error = ''
    try:
        c =  mysql.connection.cursor()
        if request.method == "POST":
            query = c.execute("SELECT * FROM users WHERE username = '{0}'" .format((request.form['username'])))
            data = c.fetchone()
            u_id = data[0]
            u_password = data[2]
            
            if sha256_crypt.verify(request.form['psw'], u_password):
                session['logged_in'] = True
                session['username'] = request.form['username']
                session['u_id'] = u_id
                flash("You are now logged in")
                return redirect(url_for("dashboard"))

            else:
                error = "Invalid credentials, try again."

        return render_template("login.html", error=error)

    except Exception as e:
        error = "Invalid credentials, try again."
        return render_template("login.html", error = error) 


@app.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    return redirect(url_for('dashboard'))
		

@app.route("/dashboard/", methods=['GET', "POST"])
def dashboard():
    error = ''
    try:
        c =  mysql.connection.cursor()
        addresses = c.execute("SELECT * FROM addresses WHERE user_id = '{0}'".format(session['u_id']))
        addresses = c.fetchall()

        if request.method == "POST":
            c.execute("INSERT INTO addresses(street, pincode, country, state, phone_number, user_id) VALUES ('{0}', {1}, '{2}', '{3}', '{4}', {5})".format((request.form['street']), (request.form['pincode']), (request.form['country']), (request.form['state']), (request.form['phone_number']), (session['u_id'])))
            mysql.connection.commit()
            c.close()
            return redirect(url_for("dashboard"))

        return render_template('dashboard.html', addresses=addresses)

    except Exception as e:
        print(str(e))
        error = "Invalid credentials, try again."
        return render_template("dashboard.html", error = error) 


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    try:
        c =  mysql.connection.cursor()
        addresses = c.execute("SELECT * FROM addresses WHERE id = {0}".format(id))
        addresses = c.fetchone()
        if request.method == 'POST':
            c.execute("UPDATE addresses SET street='{0}', pincode={1}, country='{2}', state='{3}', phone_number='{4}' WHERE user_id={5} and id={6}".format((request.form['street']), (request.form['pincode']), (request.form['country']), (request.form['state']), (request.form['phone_number']), (session['u_id']), (id)))
            mysql.connection.commit()
            c.close()
            return redirect(url_for('dashboard'))
    
        return render_template('update.html', addr=addresses)

    except Exception as e:
        print(str(e))
        return 'There was an issue updating your task'



@app.route('/delete/<int:id>')
def delete(id):
    try:
        c =  mysql.connection.cursor()
        c.execute("DELETE FROM addresses WHERE id = '{0}' and user_id = {1}".format((id), (session['u_id'])))
        mysql.connection.commit()
        c.close()
        return redirect(url_for('dashboard'))

    except:
        return 'There was a problem deleting that task'


if __name__ == "__main__":
    app.run(debug=True)

