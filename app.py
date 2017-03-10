'''
Created on Feb 16, 2017

@author: Kyle
'''

from flask import Flask, render_template, request
from flaskext.mysql import MySQL
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy

mysql = MySQL()
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:jack8998@localhost/appgen'
# db = SQLAlchemy(app)

# class application_store(db.Model):
#     __tablename__ = 'application_store'
#     id = db.Column('id_ApplicationStore', db.Integer, primary_key=True)
#     name_ApplicationStore = db.Column('name_ApplicationStore', db.Unicode)

app.debug = True
app.config['SECRET_KEY'] = 'secretkey'
toolbar = DebugToolbarExtension(app)


app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'jack8998'
app.config['MYSQL_DATABASE_DB'] = 'db_appstore'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def main():
    return render_template("index.html")

# @app.route('/home/')
# def home():
#     appName = request.form['InputBox']
#     return render_template("home.html")

@app.route('/home/', methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':
        name = request.form['storename']
        #query to db

        # cursor = mysql.connect().cursor()
        # cursor = mysql.get_db().cursor()
        # # not working ->query = "INSERT INTO testme (id,name) VALUES ('7','9')"
        # query = "INSERT INTO potlala (id, name, email) VALUES ('2222', 'Maria',  'mariaz@activestate.com')"
        # cursor.execute(query)

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO appstore_list (name) VALUES (%s)",(name))

        # me = 'testy'
        # db.session.add(me)

        conn.commit()


        return render_template("home.html", name=name)
    elif request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM appstore_list ORDER BY id DESC LIMIT 1")
        name=cursor.fetchone()[0]
        return render_template("home.html", name=name)



@app.route('/createapp/')
def createapp():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM appstore_list ORDER BY id DESC LIMIT 1")
    name=cursor.fetchone()[0]
    appname = 'Application 1'
    return render_template("createapp.html", name=name, appname=appname)

@app.route('/applist/', methods = ['POST', 'GET'])
def applist():
    conn = mysql.connect()
    cursor = conn.cursor()
    #This gets the appStore name which displays at the top
    cursor.execute("SELECT name FROM appstore_list ORDER BY id DESC LIMIT 1")
    appstore_name=cursor.fetchone()[0]
    #This gets the appStore ID which is hidden
    cursor.execute("SELECT id FROM appstore_list ORDER BY id DESC LIMIT 1")
    appstore_id=cursor.fetchone()[0]

    if request.method == 'POST':
        appName = request.form['appName']
        userReviews = request.form['reviews']
        downloadCount = request.form['downloadCount']
        verifiedDeveloper = request.form['verifiedDeveloper']
        paidApp = request.form['paid']
        rating = 3.5

        cursor.execute("INSERT INTO app_list (appstore_id, app_name, app_reviews, app_rating, app_download, app_verified, app_paid) VALUES (%s, %s, %s, %s, %s, %s, %s)",(appstore_id, appName, userReviews, rating, downloadCount, verifiedDeveloper, paidApp))
        conn.commit()

    cursor.execute("SELECT app_download FROM app_list ORDER BY id DESC LIMIT 1")
    download=cursor.fetchone()[0]

    return render_template("applist.html", name=appstore_name, appstore_id=appstore_id, download=download)

@app.route('/editapp/')
def editapp():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM appstore_list ORDER BY id DESC LIMIT 1")
    name=cursor.fetchone()[0]

    cursor.execute("SELECT app_reviews FROM app_list ORDER BY id DESC LIMIT 1")
    review=cursor.fetchone()[0]
    cursor.execute("SELECT app_download FROM app_list ORDER BY id DESC LIMIT 1")
    download=cursor.fetchone()[0]
    cursor.execute("SELECT app_verified FROM app_list ORDER BY id DESC LIMIT 1")
    developer=cursor.fetchone()[0]
    cursor.execute("SELECT app_paid FROM app_list ORDER BY id DESC LIMIT 1")
    paid=cursor.fetchone()[0]

    if review=='true':
        setReview='active'
        reviewOpp='false'
    else:
        setReview=''
        reviewOpp='true'

    if developer=='true':
        setDeveloper='active'
        developerOpp='false'
    else:
        setDeveloper=''
        developerOpp='true'
    if paid=='true':
        setPaid='active'
        paidOpp='false'
    else:
        setPaid=''
        paidOpp='true'

    return render_template("editapp.html", name=name, setReview=setReview, review=review, reviewOpp=reviewOpp, download=download, setDeveloper=setDeveloper, developer=developer, developerOpp=developerOpp, setPaid=setPaid, paid=paid, paidOpp=paidOpp)

@app.route('/addpermissionslist/')
def addpermissionslist():
    return render_template("addpermissionslist.html")

@app.route('/addpermissions/')
def addpermissions():
    return render_template("addpermissions.html")


if __name__ == "__main__":
    app.run()
