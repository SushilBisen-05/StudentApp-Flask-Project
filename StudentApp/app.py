
from flask import Flask ,render_template,request,jsonify,url_for, redirect

import pymysql
pymysql.install_as_MySQLdb()

from flask_mysqldb import MySQL


app=Flask(__name__)


#MySQL Connection with Flask

app.config['MYSQL_DB']='student'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='root'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_PORT']=3306

mysql=MySQL(app)

#Display Index Page

@app.route("/")
def index():
    return render_template('index.html')


#Display Registration Page
@app.route("/reg")
def regPage():
    return render_template("registration.html")


#Save the Data Registration page

@app.route("/saveReg",methods=['GET','POST'])
def regSaveData():
    if request.method=='POST':
        rollNo=request.form['srollNo']
        name=request.form['sname']
        course=request.form['scourse']
        duration=request.form['sduration']
        addr=request.form['saddr']

        cursor=mysql.connection.cursor()
        sql="insert into students(srollNo,sname,scourse,sduration,saddr) values(%s,%s,%s,%s,%s)"
        cursor.execute(sql,(rollNo,name,course,duration,addr))
        mysql.connection.commit()

        msg="Registration Successfully Done"
        
    return render_template("index.html",msg=msg)



#Display all User Data to FrontEnd
@app.route("/show")
def showPage():
      cursor=mysql.connection.cursor()
      cursor.execute("select * from students")
      student=cursor.fetchall()
      return render_template("view.html", student=student)


#Delete User data
@app.route("/delete/<int:srollNo>")
def DeleteStudent(srollNo):
    cursor=mysql.connection.cursor()
    sql="delete from students where srollNo=%s"
    cursor.execute(sql,(srollNo,))
    mysql.connection.commit()
    return redirect(url_for('showPage'))



#edit User data
@app.route("/edit/<int:srollNo>")
def EditStudent(srollNo):
    cursor=mysql.connection.cursor()
    sql="select * from students where srollNo=%s"
    cursor.execute(sql,(srollNo,))
    student=cursor.fetchone()
    mysql.connection.commit()
    return render_template("edit.html",student=student)
    

#update User Data
@app.route("/update",methods=['POST'])
def UpdateStudent():
    if request.method=='POST':
        srollNo=request.form['srollNo']
        sname=request.form['sname']
        scourse=request.form['scourse']
        sduration=request.form['sduration']
        saddr=request.form['saddr']

        cursor=mysql.connection.cursor()
        sql="update students set sname=%s, scourse=%s, sduration=%s, saddr=%s where srollNo=%s"
        cursor.execute(sql,(sname,scourse,sduration,saddr,srollNo))
        mysql.connection.commit()
        msg="Data Updated Successfully"

    return redirect(url_for('showPage'))


if __name__=='__main__':
    app.run(debug=True)
