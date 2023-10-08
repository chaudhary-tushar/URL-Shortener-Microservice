from flask import render_template, app, Flask, redirect

app=Flask(__name__,static_folder='templates')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["GET"])
def login():
    return redirect("http://127.0.0.1:5001/login")


if __name__=='__main__':
    app.run(debug=True)