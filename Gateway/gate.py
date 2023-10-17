from flask import render_template, app, Flask, redirect
import psycopg2, os


app=Flask(__name__,static_folder='templates')


def get_conn():
    conn=psycopg2.connect(database=os.environ.get("PSQL_DB"),  
                        user= os.environ.get("PSQL_USER"), 
                        password= os.environ.get("PSQL_PASSWORD"), 
                        host= os.environ.get("PSQL_HOST"), 
                        port= os.environ.get("PSQL_PORT"))
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["GET"])
def login():
    return redirect(f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login")   

@app.route("/profile/<int:id>")
def profile(id):
    conn=get_conn()
    cur=conn.cursor()
    cur.execute('select is_logged_in from users where id=%s;',[id])
    stst=cur.fetchone()[0]
    if stst==True:
        return redirect(f"http://{os.environ.get('PROFILE_SVC_ADDRESS')}/profile/{id}")   
    else:
        return redirect(f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login")   
    
@app.route('/<id>')
def url_redirect(id):
    print("got till here")
    return redirect(f"http://{os.environ.get('REDIRECT_SVC_ADDRESS')}/redirect/{id}")  


if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080)