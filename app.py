 # Create a new python file named "flask"
import os
from flask import Flask, jsonify
from flask import render_template, url_for, flash, request, redirect, Response
import sqlite3
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from forms import LoginForm
from text_cleaning import text_cleaning
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
app = Flask(__name__)
app.debug=True
login_manager = LoginManager(app)
login_manager.login_view = "login"
app.secret_key = 'the random string'
email=""
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = 'static/uploads/'
colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
class User(UserMixin):
    def __init__(self, id, email, password):
         self.id = str(id)
         self.email = email
         self.password = password
         self.authenticated = False
    def is_active(self):
         return self.is_active()
    def is_anonymous(self):
         return False
    def is_authenticated(self):
         return self.authenticated
    def is_active(self):
         return True
    def get_id(self):
         return self.id
@login_manager.user_loader
def load_user(user_id):
   conn = sqlite3.connect('database.db')
   curs = conn.cursor()
   curs.execute("SELECT * from login where user_id = (?)",[user_id])
   lu = curs.fetchone()
   if lu is None:
      return None
   else:
      return User(int(lu[0]), lu[1], lu[2])
@app.route("/", methods=['GET'])
def home():
     return render_template('home.html')

@app.route("/login", methods=['GET','POST'])
def login():
  form = LoginForm()
  global email
  email =form.email.data

  if current_user.is_authenticated:
     con=sqlite3.connect('database.db')
     cur=con.cursor()
     cur.execute("SELECT * FROM dairy where email = (?)",    [email])
     user = list(cur.fetchall())
     print(user)
     # return  render_template('profile_f.html',email=email)
     return redirect("/Insert")

  if form.validate_on_submit():
     conn = sqlite3.connect('database.db')
     curs = conn.cursor()
     curs.execute("SELECT * FROM login where email = (?)",    [form.email.data])
     user = list(curs.fetchone())
     Us = load_user(user[0])
     if form.email.data == Us.email and form.password.data == Us.password:
        login_user(Us, remember=form.remember.data)
        Umail = list({form.email.data})[0].split('@')[0]
        flash('Logged in successfully '+Umail)
        #return render_template('profile_f.html',email=Umail)
        return redirect("/Insert")
     else:
        flash('Login Unsuccessfull.')
  return render_template('login.html',title='Login', form=form)
@app.route("/logout", methods=["GET"])
@login_required
def logout():
     user = current_user
     user.authenticated = False
     logout_user()
     flash('Logout successfull.')
     return  redirect("/login")
@app.route("/register", methods=['GET','POST'])
def register():
     if request.method == 'GET':
          return  render_template('register.html')
     if request.method == 'POST':
          msg=""
          user_id=request.form['email']
          pwd=request.form['pwd']
          conn = sqlite3.connect('database.db')
          curs = conn.cursor()
          curs.execute("SELECT count(*) FROM login where email = (?)",    [user_id])
          num = int(list(curs.fetchone())[0])
          curs.execute("SELECT count(*) FROM login")
          total_count=int(list(curs.fetchone())[0])
          if num>0:
               msg='user already exists'
          elif  total_count>10:
               msg="sorry , user limit has reached . contact admin!!"    
          else:
               # print('good')
               curs.execute("INSERT INTO login(email,password) VALUES(?,?)",    [user_id,pwd])
               conn.commit()      
               curs.close()
               msg="Hey!! You have been registered"

     # print(user_id+'hi')
     return render_template('register.html',msg=msg)
@app.route("/admin", methods=['GET','POST'])
@login_required
def admin(): 
     global email
     conn = sqlite3.connect('database.db')
     curs = conn.cursor()
     curs.execute("SELECT email,password FROM login ")
     user = curs.fetchall()
     data=[list(i) for i  in user]
     if email=='admin@gmail.com':
          return render_template('admin.html',data=data)
     else:
          flash('sorry u dont have access')  
     return redirect('/login')       


@app.route("/email_check", methods=['GET','POST'])
def email_check():  
    if request.method == 'POST':
          msg=""
          user_id=request.form['email']
          pwd=request.form['pwd']
          conn = sqlite3.connect('database.db')
          curs = conn.cursor()
          curs.execute("SELECT count(*) FROM login where email = (?)",    [user_id])
          num = int(list(curs.fetchone())[0])
          print('hers')
          if num>0:
               msg='user already exists'
               print(msg)
          # else:
          #      print('good')
          #      curs.execute("INSERT INTO login(email,password) VALUES(?,?)",    [user_id,pwd])
          #      conn.commit()      
          #      curs.close()
          #      msg="You have been registered"


    return msg  
@app.route("/Insert", methods=['GET','POST'])
@login_required
def Insert():
     global email,colors
     print(str(email)+"lemail")
     # text=str(request.form['fname'])
     conn = sqlite3.connect('database.db')
     curs = conn.cursor()
     curs.execute("SELECT count(text) FROM dairy where email = (?)",    [email])
     num = int(list(curs.fetchone())[0])
     print(num)
     if  email is None or len(email)==0  :
          return redirect("/logout")
     # elif  num>7:
     #      print('reached limit')  
     # else :
     #      curs.execute("INSERT INTO dairy(email,text) VALUES(?,?)",    [email,text])
     #      conn.commit()
     curs.execute("SELECT diary_id,text FROM dairy where email = (?)",    [email])
     user = curs.fetchall()
     data=[list(i) for i  in user]
     conn.close()
     note=[i[1] for i in data]
     output=text_cleaning(note)
     output=pd.DataFrame(output)
     pyt={'values' : list(output.value_counts()),
     'labels' : list(output.value_counts().index),
     'colors': colors[0:int(output.nunique())]}
     
     # if len(text) !=0:
          
     #      plt.pie(output.value_counts(), labels =output.value_counts().index, autopct='%.0f%%')
     #      os.remove(os.path.join(basedir,UPLOAD_FOLDER,'fig.jpg'))
     #      plt.savefig(os.path.join(basedir,UPLOAD_FOLDER,'fig.jpg'), dpi=300)
     
     return  render_template('profile_f.html',data=data,email='Welocome '+email.split('@')[0],pyt=pyt)
@app.route('/display_stat/<filename>')
def display_stat(filename):
	return redirect(url_for('static',filename='uploads/' + 'fig.jpg'))

@app.route('/edit',methods=['GET','POST'])
def edit():
     conn = sqlite3.connect('database.db')
     curs = conn.cursor()
     if request.method == 'POST':
        print('edit')
        text = str(request.form['text'])
        id = request.form['string']
        if text.replace(" ", "") == '':
            msg = '!Its empty!! Please Input Notes'  
        else:  
          curs.execute("UPDATE dairy SET text = (?) WHERE diary_id = (?) ", [text, id])
          conn.commit()      
          curs.close()
          msg = 'Record successfully Updated'   
     
     return jsonify(msg)    
@app.route("/add",methods=["POST","GET"])
def add():
     global email
     conn = sqlite3.connect('database.db')
     curs = conn.cursor()
     if request.method == 'POST':
        txtname = request.form['text']
        if txtname == '':
            msg = 'Its empty!! Please Input Notes'  
        else:        
            curs.execute("SELECT count(text) FROM dairy where email = (?)",    [email])
            num = int(list(curs.fetchone())[0])
            print(num)
            if  len(email)==0  :
               return redirect("/logout")
            elif  num>10:
               msg = 'Reached limit , Delete notes to add new' 
            else :
               curs.execute("INSERT INTO dairy(email,text) VALUES(?,?)",    [email,txtname])
               conn.commit()
               msg = 'New record created successfully!!'   
     return jsonify(msg)

@app.route("/delete",methods=["POST","GET"])     
def delete():
    conn = sqlite3.connect('database.db')
    curs = conn.cursor()
    if request.method == 'POST':
        id = int(request.form['string'])
        print(id)
        curs.execute("SELECT count(text) FROM dairy where email = (?)",    [email])
        num = int(list(curs.fetchone())[0])
        if num<=1:
          curs.execute('update dairy set Text="" WHERE diary_id = (?)' ,[id])
        else:
          curs.execute('DELETE FROM dairy WHERE diary_id = (?)' ,[id])
          conn.commit()       
          curs.close()

        msg = '!! Record deleted successfully'   
    return jsonify(msg) 
@app.route("/delete_user",methods=["POST","GET"])     
def delete_user():
     conn = sqlite3.connect('database.db')
     curs = conn.cursor()
     if request.method == 'POST':
        id = str(request.form['string'])
        print(id)
        curs.execute('DELETE FROM login WHERE email = (?)' ,[id])
        conn.commit()       
        curs.close()
        msg = '!! user deleted successfully'   
     return jsonify(msg) 
if __name__ == "__main__":
  app.run(debug=True,port=5000)
