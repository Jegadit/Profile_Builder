import os
import json
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from datetime import datetime
import pymysql
import hashlib



application = Flask(__name__)
app = application
app.secret_key = 'AshbornIsLegend'

rnoo = ''

mydb = pymysql.connect(
    host="softareeng.cfr7joesroih.us-east-1.rds.amazonaws.com",
    user="admin",
    passwd="password123",
    database="softareeng"
)

# mydb = pymysql.connect(
#     host="localhost",
#     user="root",
#     passwd="",
#     database="SoftareEng"
# )

def hash_string(string):
    hash_object = hashlib.sha256()
    hash_object.update(string.encode('utf-8'))
    return hash_object.hexdigest()


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=['POST', 'GET'])
def login():

    if request.method == "POST":

        if request.form.get("uname", False):
            user = request.form["uname"]
            passwd = hash_string(request.form["passwd"])

            errorcode = ""

            global roll
            roll = user

            rnoo = roll


            loginpart = mydb.cursor()
            loginpart.execute(
                "SELECT role, uname FROM login WHERE ROLLNO = %s AND passw = %s", (user, passwd))
            loginresult = loginpart.fetchall()
            print(loginresult)
            # loginresult = 1

            global unme 
            unme = loginresult[0][1]

            if loginresult:
                session["user"] = loginresult[0][1]
                global desig 
                desig = loginresult[0][0]
                return redirect(url_for("user"))
            else:
                errorcode = "Invalid Username or Password"
                return render_template('login.html', errorcode=errorcode)
        
        if request.form.get('p1', False) == request.form.get('p1c', False):
            
            un = request.form['luname'] 
            rn = request.form['lrno']
            role = request.form['role']
            passd = hash_string(request.form['p1'])

            cur = mydb.cursor()
            sql = "INSERT INTO login (UNAME, ROLLNO, ROLE, PASSW) VALUES (%s, %s, %s, %s)"
            cur.execute(sql, (un, rn, role, passd))
            mydb.commit()

            return render_template('login.html')

    else:
        return render_template("login.html")


@app.route("/user", methods=['POST', 'GET'])
def user():
    if 'user' in session:

        if request.method == "POST":
            
            searchroidb = mydb.cursor()
            searchroidb.execute("SELECT distinct f_roi FROM facultydetailsleveltwo;")
            searchroiresult = searchroidb.fetchall()

            fname = request.form.get("facname", False)
            froi = request.form.get("roi", False)

            print(fname, froi)

            if fname and froi == 'Research Interest not found.':
                searchfltdb =mydb.cursor()
                searchfltdb.execute("SELECT distinct f_name, f_image, f_position, f_link FROM facultydetailsleveltwo WHERE f_name = %s", (fname))
                searchfltres = searchfltdb.fetchall()
                print(searchfltres)
                return render_template("search.html", finfo = searchfltres , roi = searchroiresult, user = session["user"])
            
            else:
                searchfltbroidb = mydb.cursor()
                searchfltbroidb.execute("select distinct f_name, f_image, f_position, f_link FROM facultydetailsleveltwo WHERE f_roi = %s", (froi))
                searchfltbroiresult = searchfltbroidb.fetchall()
                print(len(searchfltbroiresult))
                return render_template("search.html", finfo = searchfltbroiresult , roi = searchroiresult, user = session["user"])



        else:
            searchnaoidb = mydb.cursor()
            searchnaoidb.execute("SELECT AOI FROM student where ROLLNO = %s", (roll))
            searchaoiresult = searchnaoidb.fetchall()
            
            searchroidb = mydb.cursor()
            searchroidb.execute("SELECT distinct f_roi FROM facultydetailsleveltwo;")
            searchroiresult = searchroidb.fetchall()

            searchfacultydb = mydb.cursor()
            searchfacultydb.execute("SELECT distinct f_name, f_image, f_position, f_link FROM facultydetailsleveltwo where f_roi = %s", (searchaoiresult))
            searchfacultyresult = searchfacultydb.fetchall()

            print(searchfacultyresult)

            return render_template("search.html", finfo = searchfacultyresult, roi = searchroiresult, user = session["user"])
    else:
        return redirect(url_for("login"))

@app.route("/myData")
def mydata():
    if 'user' in session:
        pass
    else:
        return redirect(url_for("login"))

@app.route("/profile/<nameid>")
def profile(nameid):
    if 'user' in session:
        pass
    else:
        return redirect(url_for("login"))


@app.route("/forum", methods=['POST', 'GET'])
def search():
    if 'user' in session:
        if request.method == "POST":

            getmsg = request.form['message']
            print(getmsg)
            
            cur = mydb.cursor()
            sql = "INSERT INTO forum (UNAME, MSSG) VALUES (%s, %s)"
            cur.execute(sql, (session["user"], getmsg))
            mydb.commit()

            forummsg = mydb.cursor()
            forummsg.execute("SELECT * FROM forum;")
            forumresult = forummsg.fetchall()

            print(forumresult)

            return render_template("forum.html", msgs = forumresult, user = session["user"])
        else:

            forummsg = mydb.cursor()
            forummsg.execute("SELECT * FROM forum;")
            forumresult = forummsg.fetchall()

            print(forumresult)
            return render_template("forum.html", msgs = forumresult, user = session["user"])
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
    app.run(debug=True)