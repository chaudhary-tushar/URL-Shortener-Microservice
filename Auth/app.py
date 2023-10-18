from flask import Flask, render_template, request, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
import psycopg2, os
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__,static_folder='templates')

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

csrf = CSRFProtect(app)

def get_conn():
    conn=psycopg2.connect(database=os.environ.get("PSQL_DB"),  
                        user= os.environ.get("PSQL_USER"), 
                        password= os.environ.get("PSQL_PASSWORD"), 
                        host= os.environ.get("PSQL_HOST"), 
                        port= os.environ.get("PSQL_PORT"))
    return conn

conn = get_conn()
cur = conn.cursor() 
  
cur.execute( 
    '''CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY NOT NULL UNIQUE, username VARCHAR(15) NOT NULL UNIQUE, email VARCHAR(255) NOT NULL UNIQUE, password VARCHAR(15) NOT NULL);''')      
conn.commit() 
cur.close() 
conn.close() 



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
    password_hash = generate_password_hash(password, method="pbkdf2:sha256")
    
    if check_password_hash(pswd[0],password_hash):
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
        cur.execute('update users set is_logged_in=True where username=%s;',[username])
        cur.execute('select id from users where username=%s;',[username])
        results=cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        id=results[0]
        return redirect(f"http://{os.environ.get('GATE_SVC_ADDRESS')}/prof/{id}") 
    return render_template("login.html",form=form)

@app.route("/signup", methods=["POST","GET"])
def signup():
    form = RegisterForm()
    if request.method=="POST" :
        email=request.form.get('email')
        username=request.form.get('Username')
        password=request.form.get('password')
        print(type(password), password)
        emessage=validate_email(email)
        umessage=validate_username(username)
        password1 = generate_password_hash(password,method="pbkdf2:sha256")
        if not emessage:
            flash("Email Taken", "error")
            return redirect('signup')
        if not umessage:
            flash("Username Taken", "error")
            return redirect('signup')
        conn=get_conn()
        cur=conn.cursor()
        cur.execute('insert into users (username, email, password) values(%s,%s,%s);',[username,email,password1])
        conn.commit()
        cur.close()
        conn.close()
        return redirect("/login")

    return render_template("register.html",form=form)

@app.route("/logout/<int:id>")
def logout(id):
    conn=get_conn()
    cur=conn.cursor()
    cur.execute('update users set is_logged_in=False where id=%s;',[id])
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/login")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)

