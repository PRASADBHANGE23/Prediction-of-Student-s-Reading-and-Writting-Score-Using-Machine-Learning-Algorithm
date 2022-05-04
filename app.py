from flask import Flask,render_template,request,url_for,redirect,session
import pickle
from sqlite3 import *
from random import randrange
from flask_mail import Mail,Message

app=Flask(__name__)

app.config["MAIL_SERVER"]= "smtp.gmail.com"
app.config["MAIL_PORT"]=587
app.config["MAIL_USERNAME"]="bhangeprasad16@gmail.com"
app.config["MAIL_PASSWORD"]="Prasad@230402"
app.config["MAIL_USE_TLS"]=True
app.config["MAIL_USE_SSL"]=False

app.secret_key="Prasadbhangerocks"

mail=Mail(app)

@app.route("/fpassword",methods=["GET","POST"])
def fpassword():
	if request.method=="POST":	
		em=request.form["em"]
		usr=request.form["usr"]	
		con=None
		try:
			con=connect("flask.db")
			cursor=con.cursor()
			sql="select password from student where username='%s'"	
			cursor.execute(sql%(usr))
			data=cursor.fetchall()
			if len(data)==0:
				return render_template("fpassword.html",msg="user dosn't exists")
			else:

				return render_template("fpassword.html",msg=data)

		except Exception as e:
			return render_template("fpassword.html",msg=e)
		finally:
			msg=Message("regarding forgotten password",sender="bhangeprasad16@gmail.com",recipients=[em])
			msg.body="Your password is " + str(data) + "\n \n \nNote:\nIf there is a empty space in the place of password,then you are new user,please signup and create your account. \n \n Thank you!!!"				
			mail.send(msg)
			if con is not None:
				con.close()
	else:
		return render_template("fpassword.html")
		

@app.route("/logout",methods=["GET","POST"])
def logout():
	session.clear()
	return redirect (url_for("login"))


@app.route("/",methods=["GET","POST"])

def home():
	if "username" in session:
		return render_template("home.html",name=session["username"])
		
	else:
		return redirect(url_for("login"))	

@app.route("/check")
def check():
	
	r1=request.args.get("r1")
	if r1=="male":
		ge=1
	else:
		ge=0

	r2=request.args.get("r2")
	if r2=="b":
		ra1=1
	else:
		ra1=0
	if r2=="c":
		ra2=1
	else:
		ra2=0
	if r2=="d":
		ra3=1
	else:
		ra3=0
	if r2=="e":
		ra4=1
	else:
		ra4=0
	if r2!="b" and r2!="c" and r2!="d" and r2!="e":
		ra5=1
	else:
		ra5=0

	r3=request.args.get("r3")
	if r3=="std":
		lu=1
	else:
		lu=0

	r4=request.args.get("r4")
	if r4=="none":
		te=1
	else:
		te=0
		
	math=float(request.args.get("math"))

	data=[[math,ge,ra1,ra2,ra3,ra4,lu,te]]
	
	with open("stu_performance.model","rb") as f:
		model=pickle.load(f)
	res=model.predict(data)
	return render_template("home.html",msg=res)

@app.route("/login",methods=["GET","POST"])
def login():
	if request.method=="POST":
		un=request.form["un"]
		pw=request.form["pw"]
		con=None
		try:
			con=connect("flask.db")
			cursor=con.cursor()
			sql="select * from student where username='%s' and password='%s'"
			cursor.execute(sql%(un,pw))
			data=cursor.fetchall()
			if len(data)==0:
				return render_template("login.html",msg="invalid login")
			else:
				session["username"]=un
				session["password"]=pw
# session madhe username gheun thevl
				return redirect(url_for("home"))
		except Exception as e:
			return render_template("login.html",msg=e)
		finally:
			if con is not None:
				con.close()
	else:
		return render_template("login.html")

@app.route("/signup",methods=["GET","POST"])
def signup():
	if request.method=="POST":
		un=request.form["un"]
		pw1=request.form["pw1"]
		pw2=request.form["pw2"]
		if pw1==pw2:
			con=None
			try:
				con=connect("flask.db")
				cursor=con.cursor()
				sql="insert into student values('%s','%s')"
				cursor.execute(sql%(un,pw1))
				con.commit()
				return redirect(url_for("login"))
			except Exception as e:
				con.rollback()
				return render_template("signup.html",msg="user already exists")
			finally:
				if con is not None:
					con.close()
		else:
			return render_template("signup.html",msg="password did not match")
	else:
		return render_template("signup.html")

if __name__=="__main__":
	app.run(debug=True,use_reloader=True)