from flask import Flask , render_template,request,jsonify,redirect,url_for
# from flask_mysql_connector import MySQL
# from flask_mysqldb import MySQL

import pymysql
pymysql.install_as_MySQLdb()

from flask_mysqldb import MySQL


app=Flask(__name__)
#con=mysql.connector.connect(user="root",password="root",host="localhost",database="product")

app.config["MYSQL_USER"]='root'
app.config["MYSQL_PASSWORD"]='root'
app.config["MYSQL_HOST"]='localhost'
app.config["MYSQL_PORT"]=3306
app.config["MYSQL_DB"]='product'

mysql=MySQL(app)

#mysql=MySQL(app)  # flask application to connect with mysql

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/savedata",methods=['GET','POST'])
def dataSave():
    if request.method=='POST':
        pid=request.form['pid']
        pname=request.form['pname']
        pcost=request.form['pcost']

        cursor=mysql.connection.cursor()            # 
        cursor.execute("insert into ptable(pid,pname,pcost) values(%s,%s,%s)",(pid,pname,pcost))
        mysql.connection.commit()

    return jsonify({"massage":"DataSave Sucessfully"})

@app.route("/show")
def sendData():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM ptable")
    p = cursor.fetchall()
    

    return render_template("show.html", p=p)

app.route("delete/<int:pid>")
def deleteData(pid):
    cursor = mysql.connection.cursor()
    cursor.execute("delete from ptable where pid=%s",(pid))
    return redirect(url_for("sendData"))
    
    


if __name__ == '__main__':
    app.run(debug=True)