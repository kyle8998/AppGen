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
app.config['MYSQL_DATABASE_DB'] = 'appgen'
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
        cursor.execute("INSERT INTO application_store (name_ApplicationStore) VALUES (%s)",(name))

        # me = 'testy'
        # db.session.add(me)

        conn.commit()


        return render_template("home.html", name=name)
    elif request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name_ApplicationStore FROM application_store ORDER BY id_ApplicationStore DESC LIMIT 1")
        name=cursor.fetchone()[0]
        return render_template("home.html", name=name)



@app.route('/createapp/')
def createapp():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT name_ApplicationStore FROM application_store ORDER BY id_ApplicationStore DESC LIMIT 1")
    name=cursor.fetchone()[0]
    return render_template("createapp.html", name=name)

@app.route('/applist/', methods = ['POST', 'GET'])
def applist():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT name_ApplicationStore FROM application_store ORDER BY id_ApplicationStore DESC LIMIT 1")
    name=cursor.fetchone()[0]

    if request.method == 'POST':
        userReviews = request.form['reviews']
        downloadCount = request.form['downloadCount']
        verifiedDeveloper = request.form['verifiedDeveloper']
        paidApp = request.form['paid']

        cursor.execute("INSERT INTO application_list (userReviews_application, downloadCount_application, verifiedDeveloper_application, paidApp_application) VALUES (%s, %s, %s, %s)",(userReviews, downloadCount, verifiedDeveloper, paidApp))


        conn.commit()

    return render_template("applist.html", name=name)

@app.route('/addpermissionslist/')
def addpermissionslist():
    return render_template("addpermissionslist.html")

@app.route('/addpermissions/')
def addpermissions():
    return render_template("addpermissions.html")


if __name__ == "__main__":
    app.run()
