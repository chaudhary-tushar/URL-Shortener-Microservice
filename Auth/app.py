from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
import psycopg2

app = Flask(__name__,static_folder='templates')
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a strong secret key
csrf = CSRFProtect(app)
conn = psycopg2.connect(database="urlauth", 
                        user="uauth_user", 
                        password="Aauth123", 
                        host="localhost", 
                        port="5432") 
cur = conn.cursor() 
  
# if you already have any table or not id doesnt matter this  
# will create a products table for you. 
cur.execute( 
    '''CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY NOT NULL UNIQUE, username VARCHAR(15) NOT NULL UNIQUE, email VARCHAR(255) NOT NULL UNIQUE, password VARCHAR(15) NOT NULL);''')      
conn.commit() 
cur.close() 
conn.close() 

def get_conn():
    conn=psycopg2.connect(database="urlauth", 
                        user="uauth_user", 
                        password="Aauth123", 
                        host="localhost", 
                        port="5432")
    return conn

class RegisterForm (FlaskForm):
    username = StringField (validators= [InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    email = StringField (validators=[InputRequired(), Length(min=4, max=20)],render_kw={"placeholder": "E-mail"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit= SubmitField("Register")
    
def validate_username(username):
        conn=get_conn()
        cur=conn.cursor()
        cur.execute('select username from users where username=%s', [username])
        result_username = cur.fetchone()
        if  result_username is not None:
            return False
        return True
def validate_email(email):
        conn=get_conn()
        cur=conn.cursor()
        cur.execute('select email from users where email=%s',[email])
        result_email=cur.fetchone()
        if result_email is not None:
            return False
        return True

def validate_login(username):
    conn=get_conn()
    cur=conn.cursor()
    cur.execute('select * from users where username=%s',[username])
    row = cur.fetchone()
    if row is None:
        return False
    return True

def validate_password(username,password):
    conn=get_conn()
    cur=conn.cursor()
    cur.execute('select password from users where username=%s;',[username])
    pswd=cur.fetchone()
    if password!=pswd[0]:
        return False
    return True



class LoginForm (FlaskForm):
    username = StringField (validators= [InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField (validators= [InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

@app.route("/login", methods=["POST","GET"])
def login():
    form = LoginForm()
    if request.method=="POST":
        username = request.form.get('Username') 
        password = request.form.get('password')
        print(username,password)
        vuser=validate_login(username)
        vpass=validate_password(username,password)
        if not vuser:
            flash("No Such User Exists!", "error")
            return redirect('/login')
        if not vpass:
            flash("wrong password given", "error")
            return redirect('/login')
        conn=get_conn()
        cur=conn.cursor()
        cur.execute('select id from users where username=%s;',[username])
        results=cur.fetchone()
        id=results[0]
        return redirect(f"http://127.0.0.1:5000/profile/{id}")
    return render_template("login.html",form=form)

@app.route("/signup", methods=["POST","GET"])
def signup():
    form = RegisterForm()
    if request.method=="POST" :
        email=request.form.get('email')
        username=request.form.get('Username')
        password=request.form.get('password')
        emessage=validate_email(email)
        umessage=validate_username(username)
        if not emessage:
            flash("Email Taken", "error")
            return redirect('signup')
        if not umessage:
            flash("Username Taken", "error")
            return redirect('signup')
        conn=get_conn()
        cur=conn.cursor()
        cur.execute('insert into users (username, email, password) values(%s,%s,%s);',[username,email,password])
        conn.commit()
        cur.close()
        conn.close()
        return redirect("/login")

    return render_template("register.html",form=form)

if __name__ == "__main__":
    app.run(port=5001)

