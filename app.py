import os
import json
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from datetime import datetime
import pymysql
# from textwrap import indent

application = Flask(__name__)
app = application
app.secret_key = 'AshbornIsLegend'
email = ''

mydb = pymysql.connect(
    host="profilebuilder.cfr7joesroih.us-east-1.rds.amazonaws.com",
    user="admin",
    passwd="Oombu1234",
    database="SoftareEng"
)

# mydb = pymysql.connect(
#     host="localhost",
#     user="root",
#     passwd="",
#     database="SoftareEng"
# )

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login", methods=['POST', 'GET'])
def login():

    if request.method == "POST":
        user = request.form["uname"]
        passwd = request.form["passwd"]

        errorcode = ""

        loginpart = mydb.cursor()
        loginpart.execute(
            "SELECT email FROM Login WHERE uname = %s AND passwd = %s", (user, passwd))
        loginresult = loginpart.fetchall()
        print(loginresult)
        # loginresult = 1

        if loginresult:
            session["user"] = loginresult[0][0]
            email = loginresult[0][0]
            return redirect(url_for("user"))
        else:
            errorcode = "Invalid Username or Password"
            return render_template('login.html', errorcode=errorcode)

    else:
        return render_template("login.html")


@app.route("/user")
def user():
    if 'user' in session:
        return 'Hello world!'
        # return render_template("os.html")
    else:
        return redirect(url_for("login"))


@app.route("/status")
def status():
    return jsonify(status="active")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run()