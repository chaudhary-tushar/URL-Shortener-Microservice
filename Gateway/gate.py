from flask import render_template, app, Flask, redirect
import psycopg2

app=Flask(__name__,static_folder='templates')

def get_conn():
    conn=psycopg2.connect(database="urlauth", 
                        user="uauth_user", 
                        password="Aauth123", 
                        host="localhost", 
                        port="5432")
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["GET"])
def login():
    return redirect("http://127.0.0.1:5001/login")

@app.route("/profile/<int:id>")
def profile(id):
    conn=get_conn()
    cur=conn.cursor()
    cur.execute('select is_logged_in from users where id=%s;',[id])
    print("workin till gate/profile redirection")
    stst=cur.fetchone()[0]
    print(stst)
    if stst==True:
        return redirect(f"http://127.0.0.1:5002/profile/{id}")
    else:
        return redirect("http://127.0.0.1:5001/login")
    
@app.route('/<id>')
def url_redirect(id):
    return redirect(f"http://127.0.0.1:5003/redirect/{id}")


if __name__=='__main__':
    app.run(debug=True,port=80)