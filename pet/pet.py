from calendar import c
from subprocess import BELOW_NORMAL_PRIORITY_CLASS
from flask import Flask, render_template, request, jsonify, Response, json, redirect,url_for,flash,session
from flask_pymongo import PyMongo, ObjectId
from flask_session import Session
import re

PET=Flask(__name__)
PET.config['MONGO_URI']="mongodb://localhost:27017/petapp"
PET.config['SECRET_KEY']='98$%^#@SECRET'
PET.config["SESSION_PERMANENT"] = False
PET.config["SESSION_TYPE"] = "filesystem"
mongo = PyMongo(PET)
sessionv=Session(PET)

db=mongo.db.users
db1=mongo.db.animals
db2=mongo.db.cart
db3=mongo.db.payments


#HOME
@PET.route("/",methods=["GET","POST"])
def home():
    return render_template("Home.html")

#SIGNUP
@PET.route("/signup",methods=["POST","GET"])
def Signup():
    if request.method=="POST":
        name=request.form['username']
        password=request.form['password']
        email=request.form['email']
        contact=request.form['contact'] 
        dist_mail=list(db.find({'email':request.form['email']}))
        if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            flash(f"Please enter a valid email id")
        elif(dist_mail):
            flash(f'"email already exists please enter a new email"','danger')

        elif not re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,10}$', password):
            flash(f"Password should contain 8-10 characters with atleast 1 uppercase letter, lowercase letter, digit, and a special character")
        else:
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
        test=list(db.find({'email':email,'password':password},{"_id":0}))
        check=list(db.find({'email':email,'password':password},{'_id':0}))
        try:
            if((test[0]['email']=='admin@gmail.com') and (test[0]['password']=='admin')):
                session["email"]=email
                flash("Welcome Admin")
                return redirect("/Admin")
            elif(list(db.find({'email':request.form['email'],'password':request.form['password']},{'_id':0}))):
                session["email"]=email
                flash(f"Logged in as: " +email)
                return redirect("/users")
        except:
            flash("INVALID LOGIN")
            return redirect("/login")
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
    if request.method=="POST":
        Breed=request.form.get('dbreed')
        Product_Name=request.form['pname']
        Product_Type=request.form.get('ptype')
        Product_Id=request.form['pid']
        Price=request.form['price']
        Expires_in=request.form['edate']
        Stock_Count=request.form['stock'] 
        Discount=request.form['disc'] 

        id=db1.insert_one({
            'Animal': 'Dog',
            'Breed':Breed,
            'Product_Name':Product_Name,
            'Product_Type':Product_Type,
            'Product_Id':Product_Id,
            'Price':Price,
            'Expires_in':Expires_in,
            'Stock_Count':Stock_Count,
            'Discount':Discount})
        flash("Data added Successfully")
    return render_template("dadd.html")

#CAT ADD
@PET.route("/Cat",methods=["GET","POST"])
def Cat():
    if request.method=="POST":
        Product_Name=request.form['pname']
        Product_Type=request.form.get('ptype')
        Product_Id=request.form['pid']
        Price=request.form['price']
        Expires_in=request.form['edate']
        Stock_Count=request.form['stock'] 
        Discount=request.form['disc'] 

        id=db1.insert_one({
            'Animal': 'Cat',
            'Breed': 'None',
            'Product_Name':Product_Name,
            'Product_Type':Product_Type,
            'Product_Id':Product_Id,
            'Price':Price,
            'Expires_in':Expires_in,
            'Stock_Count':Stock_Count,
            'Discount':Discount})
        flash("Data added Successfully")
    return render_template("cadd.html")


#Parrot ADD
@PET.route("/Parrot",methods=["GET","POST"])
def Parrot():
    
    if request.method=="POST":
        Breed=request.form.get('breed')
        Product_Name=request.form['pname']
        Product_Type=request.form.get('ptype')
        Product_Id=request.form['pid']
        Price=request.form['price']
        Expires_in=request.form['edate']
        Stock_Count=request.form['stock'] 
        Discount=request.form['disc'] 

        id=db1.insert_one({
            'Animal': 'Bird',
            'Breed':Breed,
            'Product_Name':Product_Name,
            'Product_Type':Product_Type,
            'Product_Id':Product_Id,
            'Price':Price,
            'Expires_in':Expires_in,
            'Stock_Count':Stock_Count,
            'Discount':Discount})
        flash("Data added Successfully")
    return render_template("padd.html")

#Turtle ADD
@PET.route("/Turtle",methods=["GET","POST"])
def turtle():
    
    if request.method=="POST":
        Product_Name=request.form['pname']
        Product_Type=request.form.get('ptype')
        Product_Id=request.form['pid']
        Price=request.form['price']
        Expires_in=request.form['edate']
        Stock_Count=request.form['stock'] 
        Discount=request.form['disc'] 

        id=db1.insert_one({
            'Animal': 'Turtle',
            'Breed': 'None',
            'Product_Name':Product_Name,
            'Product_Type':Product_Type,
            'Product_Id':Product_Id,
            'Price':Price,
            'Expires_in':Expires_in,
            'Stock_Count':Stock_Count,
            'Discount':Discount})
        flash("Data added Successfully")
    return render_template("tadd.html")

   
#INVENTORY
@PET.route("/inventory",methods=["GET","POST"])
def Inventory():
    Animal=request.form.get('Animal')
    det=[]
    if request.method=="POST":
        if (list((db1.find({'Animal':Animal})))):
            data=(list((db1.find({'Animal':Animal}))))
            for i in data:
                det.append(i)
        else:
            flash(f"Sorry no products found")

    return render_template("inventory.html",det=det)

#ADMIN DELETE   
@PET.route("/delete/<id>",methods=["GET","POST"])
def dele(id):
    if 'email' in session:
        db1.delete_one({'_id':ObjectId(id)})
    return redirect(url_for('Inventory'))

#CART DELETE   
@PET.route("/cdelete/<id>",methods=["GET","POST"])
def cdele(id):
    if 'email' in session:
        db2.delete_one({'_id':ObjectId(id)})
        return render_template('cart.html')

#ADMIN UPDATE
@PET.route("/update/<id>",methods=["POST"])
def update(id):
    print(id)
    if request.method=="POST":
        yy = db1.update_many({'_id':ObjectId(id)},  { "$set": {'Breed':request.form.get('breed'),'Expires_in':request.form.get('edate'),'Product_Name':request.form['pname'],'Product_Type':request.form['ptype'],'Product_Id':request.form['pid'],'Price':request.form['price'],'Stock_Count':request.form['stock'],'Discount':request.form['disc']}})
    return redirect(url_for('Inventory'))

#USERS
@PET.route("/users",methods=["GET","POST"])
def users():
    d = []
    d1= []
    data = list(db1.find({'Product_Name': 'Pedigree'}))
    for i in data:
        d.append(i)
    print(d)
    data1 = list(db1.find({'Product_Name': 'Wobble Wag Giggle Ball'}))
    for i in data1:
        d1.append(i)
    return render_template("user.html",d=d, d1 = d1)

#SIDENAV
@PET.route("/sidenav",methods=["GET","POST"])
def sidenav():
    return render_template("sidenav.html")

#SIDENAV
@PET.route("/navbar",methods=["GET","POST"])
def navbar():
    return render_template("navbar.html")

@PET.route('/dummy')
def dummy():
    return render_template('dummynav.html')

@PET.route("/checkout")
def checkout():
    return render_template("checkout.html")

@PET.route('/userdata',methods = ['GET','POST'])
def Userdata():
    udet = []
    data = list(db.find({'Product_Name':'Wobble Wag Giggle Ball'}))
    for i in data:
        udet.append(i)       
    return render_template('userdata.html',udet=udet)

@PET.route('/Purchased',methods = ['GET','POST'])
def Purchaseditems():   
    return render_template('apurchased.html')

@PET.route('/inven',methods = ['GET','POST'])
def Inven():   
    return render_template('inven.html')


@PET.route('/cart')
def cart1():
    c1=[]
    if 'email' in session:
        data=list(db2.find({}))
        for i in data:
            c1.append(i) 
    return render_template('cart.html',c1=c1)

@PET.route('/cart/<id>',methods = ['GET','POST'])
def cart(id):
    c=[]
    c1=[]
    if 'email' in session:
        cdata = list(db1.find({"_id":ObjectId(id)}))
        for i in cdata:
            c.append(i)
        print(c)
        id=db2.insert_one({
            'cid': ObjectId(id),
            'Animal': c[0]['Animal'],
            'Product_Name': c[0]['Product_Name'],
            'Product_Type': c[0]['Product_Type'],
            'Price':c[0]['Price'],
            'Discount':c[0]['Discount'],
            'count':1
        })
        data=list(db2.find({}))
        print(data)
        for i in data:
            c1.append(i)  
    return render_template('cart.html',c1=c1)
if __name__ == "__main__":
    PET.run(debug=True,port=2027)