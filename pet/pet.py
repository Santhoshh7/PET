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
db1=mongo.db.admin


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
        test=list(db.find({'email':request.form['email'],'password':request.form['password']},{"_id":0,"username":0}))
        check=list(db.find({'email':request.form['email'],'password':request.form['password']},{'name':0,'password':0,"_id":0,"email":0,"contact":0}))
        if(test):
            session["email"]=email
            return redirect("/")
        else:
            flash("INVALID LOGIN")
    return render_template("Login.html")


#LOGOUT
@PET.route("/logout",methods=["GET","POST"])
def Logout():
    session["email"]=None
    return redirect("/home")
    


if __name__ == "__main__":
    PET.run(debug=True,port=2027)