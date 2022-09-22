from calendar import c
from subprocess import BELOW_NORMAL_PRIORITY_CLASS
from flask import Flask, render_template, request, jsonify, Response, json, redirect,url_for,flash,session
from flask_pymongo import PyMongo, ObjectId
from flask_session import Session

PET=Flask(__name__)
PET.config['MONGO_URI']="mongodb://localhost:27017/petapp"
PET.config['SECRET_KEY']='98$%^#@SECRET'
PET.config["SESSION_PERMANENT"] = False
PET.config["SESSION_TYPE"] = "filesystem"
mongo = PyMongo(PET)
sessionv=Session(PET)

db=mongo.db.users
db1=mongo.db.animals
db2=mongo.db.sales


#HOME
@PET.route("/",methods=["GET","POST"])
def home():
    return render_template("Home.html")

#SIGNUP
@PET.route("/signup",methods=["POST","GET"])
def Signup():
    if request.method=="POST": 
        dist_mail=list(db.find({'email':request.form['email']}))
        if(dist_mail):
            flash(f'"email already exists please enter a new email"','danger')
        else:
            name=request.form['username']
            password=request.form['password']
            email=request.form['email']
            contact=request.form['contact']
            id=db.insert_one({
                'name':name,
                'email':email,
                'password':password,
                'contact':contact
            })
            flash("Signup Succesful")
            return redirect("/")
    return render_template("Signup.html")

#LOGIN
@PET.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form['email']
        password=request.form['password']
        test=list(db.find({'email':"admin@gmail.com",'password':"admin"},{"_id":0}))
        check=list(db.find({'email':request.form['email'],'password':request.form['password']},{'_id':0}))
        if(test):
            session["email"]=email
            flash("Welcome Admin")
            return redirect("/Admin")
        elif(check):
            session["email"]=email
            flash(f"Logged in as: " +email)
            return redirect("/users")
        else:
            flash("INVALID LOGIN")
    return render_template("Login.html")


#LOGOUT
@PET.route("/logout",methods=["GET","POST"])
def Logout():
    session["email"]=None
    return redirect("/")

#ADMIN PAGE

@PET.route("/Admin",methods=["GET","POST"])
def Admin():
    return render_template("admin.html")
    
#CHOOSE ANIMALS
@PET.route("/Animals",methods=["GET","POST"])
def Animal():
    return render_template("admin.html")

#DOG ADD
@PET.route("/Dog",methods=["GET","POST"])
def Dog():
    return render_template("dadd.html")

#CAT ADD
@PET.route("/Cat",methods=["GET","POST"])
def Cat():
    return render_template("cadd.html")


#Parrot ADD
@PET.route("/Parrot",methods=["GET","POST"])
def Parrot():
    return render_template("padd.html")

#Turtle ADD
@PET.route("/Turtle",methods=["GET","POST"])
def turtle():
    return render_template("tadd.html")

   
#ADD
@PET.route("/add")
def Add():
    return render_template("add.html")

@PET.route("/users")
def Dummy():
    return render_template("user.html")

@PET.route("/sidenav")
def sidenav():
    return render_template("sidenav.html")

@PET.route("/checkout")
def checkout():
    return render_template("checkout.html")

@PET.route('/userdata',methods = ['GET','POST'])
def Userdata():
    new_taskk_history = []
    total_history = list(db.find({},{"name":1,"email":1,"contact":1,"_id":0}))
    for i in total_history:
        new_taskk_history.append(i)       
    return render_template('userdata.html',new_task_history = new_taskk_history)

@PET.route('/Purchased',methods = ['GET','POST'])
def Purchaseditems():   
    return render_template('apurchased.html')

if __name__ == "__main__":
    PET.run(debug=True,port=2027)