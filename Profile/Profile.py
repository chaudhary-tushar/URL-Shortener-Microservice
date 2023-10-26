from flask import render_template, app, Flask, redirect,request, url_for, flash
from flask_wtf.csrf import CSRFProtect
import psycopg2, os
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_wtf import FlaskForm
from random import choice
import string


app=Flask(__name__,static_folder='templates')
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

csrf = CSRFProtect(app)

def get_conn():
    conn=psycopg2.connect(database=os.environ.get("PSQL_DB"),  
                        user= os.environ.get("PSQL_USER"), 
                        password= os.environ.get("PSQL_PASSWORD"), 
                        host= os.environ.get("PSQL_HOST"), 
                        port= os.environ.get("PSQL_PORT"))
    return conn

def shorting(strrl,id):
    conn=get_conn()
    cur=conn.cursor()
    shrt=''.join(choice(string.ascii_letters+string.digits) for _ in range(6))
    shorty = "tri.me/" + shrt
    cur.execute('INSERT INTO urldirects (user_id,long_url,short_url) VALUES (%s,%s,%s);',[id,strrl,shrt])
    conn.commit()
    cur.close()
    conn.close()
    return shorty
    
class UrlForm (FlaskForm):
    url = StringField (validators= [InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    submit = SubmitField("Login")
@app.route('/profile/<int:id>',methods=["GET","POST"])
def profile(id):
    form = UrlForm()
    cur = get_conn().cursor()   
    cur.execute('select url_id,long_url,short_url,clicks,user_id from urldirects where user_id=%s;',[id])
    rows = cur.fetchall()
    cur.execute('select username from users where id=%s;',[id])
    name=cur.fetchone()[0]
    if request.method=="POST":
        longrl = request.form.get('url') 
        shortrl=shorting(longrl,id)
        flash(f'The shortened url is {shortrl}')
        return render_template('index.html',data=rows,username=name,user_id=id,form=form)
    return render_template("index.html",data=rows,username=name,user_id=id,form=form)


@app.route('/delete/<int:uid>/<int:id>')
def deletelink(id,uid):
    conn=get_conn()
    cur=conn.cursor()
    cur.execute('DELETE FROM urldirects WHERE url_id=%s;',[id])
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("profile",id=uid))

@app.route('/<id>')
def reroute(id):
    url=f"tri.me/{id}"
    return redirect(f"http://{os.environ.get('GATE_SVC_ADDRESS')}/{id}")

@app.route('/logout/<int:id>')
def logout(id):
    return redirect(f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login")


if __name__=='__main__':
    app.run(host='0.0.0.0',port=6000)