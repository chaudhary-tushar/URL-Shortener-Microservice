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
    app.run(debug=True,port=5003)