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


@app.route("/redirect/<id>")
def reroute(id):
    
    print(id)
    try:
        conn=get_conn()
        cur=conn.cursor()
        print("entered try block")
        cur.execute('select long_url,clicks from urldirects where short_url=%s;',[id])
        udata=cur.fetchone()
        print(udata)
        clicks=udata[1]
        route=udata[0]
        print(route)
        cur.execute("update urldirects set clicks=%s where short_url=%s;",[clicks+1,id])
        conn.commit()
        cur.close()
        conn.close()
        return redirect(route)
    except :
        
        return render_template("404.html")

if __name__=='__main__':
    app.run(host='0.0.0.0',port=7000)