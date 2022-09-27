from flask import Flask, render_template, request, jsonify, Response, json, redirect,url_for,flash,session
import flask
from flask_pymongo import PyMongo, ObjectId
from flask_session import Session
import re
import flask

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
db4= mongo.db.orders


#HOME
@PET.route("/")
def home():
    return flask.render_template("Home.html")

#SIGNUP
@PET.route("/signup",methods=["GET","POST"])
def Signup():
    if flask.request.method=="POST":
        name=flask.request.form['username']
        password=flask.request.form['password']
        email=flask.request.form['email']
        contact=flask.request.form['contact'] 
        address=flask.request.form['address']
        dist_mail=list(db.find({'email':flask.request.form['email']}))
        if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            flask.flash(f"Please enter a valid email id")
        elif(dist_mail):
            flask.flash(f'"email already exists please enter a new email"','danger')

        elif not re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,10}$', password):
            flask.flash(f"Password should contain 8-10 characters with atleast 1 uppercase letter, lowercase letter, digit, and a special character")
        else:
            id=db.insert_one({
                'name':name,
                'email':email,
                'password':password,
                'contact':contact,
                'address':address
            })
            flask.flash("Signup Succesful")
            return flask.redirect("/")
    return flask.render_template("Signup.html")

#LOGIN
@PET.route("/login",methods=["GET","POST"])
def login():
    if flask.request.method=="POST":
        email=flask.request.form['email']
        password=flask.request.form['password']
        test=list(db.find({'email':email,'password':password},{"_id":0}))
        check=list(db.find({'email':email,'password':password},{'_id':0}))
        try:
            if((test[0]['email']=='admin@gmail.com') and (test[0]['password']=='admin')):
                session["email"]=email
                flash("Welcome Admin")
                return redirect("/Admin")
            elif(list(db.find({'email':flask.request.form['email'],'password':flask.request.form['password']},{'_id':0}))):
                session["email"]=email
                flash(f"Logged in as: " +email)
                return redirect("/users")
        except:
            flash("INVALID LOGIN")
            return flask.redirect("/login")
    return flask.render_template("Login.html")


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
    if flask.request.method=="POST":
        Breed=flask.request.form.get('dbreed')
        Product_Name=flask.request.form['pname']
        Product_Type=flask.request.form.get('ptype')
        Product_Id=flask.request.form['pid']
        Price=flask.request.form['price']
        Expires_in=flask.request.form['edate']
        Stock_Count=flask.request.form['stock'] 
        Discount=flask.request.form['disc'] 

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
        # x=db.update_many({}, [ {"$set":{ "price" : {"$toInt": "$price"}}} ], {"multi":True})
    return render_template("dadd.html")

#CAT ADD
@PET.route("/Cat",methods=["GET","POST"])
def Cat():
    if flask.request.method=="POST":
        Product_Name=flask.request.form['pname']
        Product_Type=flask.request.form.get('ptype')
        Product_Id=flask.request.form['pid']
        Price=flask.request.form['price']
        Expires_in=flask.request.form['edate']
        Stock_Count=flask.request.form['stock'] 
        Discount=flask.request.form['disc'] 

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
    
    if flask.request.method=="POST":
        Breed=flask.request.form.get('breed')
        Product_Name=flask.request.form['pname']
        Product_Type=flask.request.form.get('ptype')
        Product_Id=flask.request.form['pid']
        Price=flask.request.form['price']
        Expires_in=flask.request.form['edate']
        Stock_Count=flask.request.form['stock'] 
        Discount=flask.request.form['disc'] 

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
    
    if flask.request.method=="POST":
        Product_Name=flask.request.form['pname']
        Product_Type=flask.request.form.get('ptype')
        Product_Id=flask.request.form['pid']
        Price=flask.request.form['price']
        Expires_in=flask.request.form['edate']
        Stock_Count=flask.request.form['stock'] 
        Discount=flask.request.form['disc'] 

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

@PET.route("/contact")
def contact():
    return render_template('contact.html')

@PET.route("/updatePassword", methods=["POST"])
def updatePassword():
    msg = ""
    x = db.find_one({'email': session['email']})
    print(x)
    user_password = flask.request.form["oldpasswd"]
    print(user_password)
    # print(x['password'])
    if x['password'] == user_password:
        new_password = flask.request.form["newpasswd"]
        db.update_one({'email': session['email']}, {
                         '$set': {'password': new_password}})
        msg = "Updated password successfully"
    else:
        msg = "Wrong password"

    return render_template("profile.html", title="User profile", message=msg, user=getUserStats())

def getUserStats():
    user_stats = {
        'name': db.find_one({'email': session['email']})['name'],
        'email': session['email']
    }
    return user_stats

@PET.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@PET.route("/deleteAccount", methods=["POST"])
def deleteUser():
    user_password = flask.request.form["passwd"]
    x = db.find_one({'email': session['email']})
    if x['password'] == user_password:
        db.delete_one({'email': session['email']})
        return redirect(url_for("Logout"))
    else:
        msg = "Wrong password. Account deletion failed."
        return render_template("profile.html", title="User profile", message=msg)

@PET.route('/request')
def request():
    return render_template('request.html')

#INVENTORY
@PET.route("/inventory",methods=["GET","POST"])
def Inventory():
    Animal=flask.request.form.get('Animal')
    det=[]
    if flask.request.method=="POST":
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
        return redirect(url_for('cart1'))

#ADMIN UPDATE
@PET.route("/update/<id>",methods=["POST"])
def update(id):
    if flask.request.method=="POST":
        yy = db1.update_many({'_id':ObjectId(id)},  { "$set": {'Breed':flask.request.form.get('breed'),'Expires_in':flask.request.form.get('edate'),'Product_Name':flask.request.form['pname'],'Product_Type':flask.request.form['ptype'],'Product_Id':flask.request.form['pid'],'Price':flask.request.form['price'],'Stock_Count':flask.request.form['stock'],'Discount':flask.request.form['disc']}})
    return redirect(url_for('Inventory'))

#USERS
@PET.route("/users",methods=["GET","POST"])
def users():
    d = []
    d1= []
    data = list(db1.find({'Product_Name': 'Pedigree'}))
    for i in data:
        d.append(i)
    data1 = list(db1.find({'Product_Name': 'Melamine Decal Bowl'}))
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
    new_taskk_history = []
    total_history = list(db.find({},{"name":1,"email":1,"contact":1,"_id":0}))
    for i in total_history:
        new_taskk_history.append(i)       
    return render_template('userdata.html',new_task_history = new_taskk_history)

@PET.route('/Purchased',methods = ['GET','POST'])
def Purchaseditems():   
    return render_template('purchased.html')

@PET.route('/inven',methods = ['GET','POST'])
def Inven():   
    return render_template('inven.html')

@PET.route('/dadd',methods = ['GET','POST'])
def dadd():   
    return render_template('dadd.html')

@PET.route('/tadd',methods = ['GET','POST'])
def tadd():   
    return render_template('tadd.html')

@PET.route('/cadd',methods = ['GET','POST'])
def cadd():   
    return render_template('cadd.html')

@PET.route('/padd',methods = ['GET','POST'])
def padd():   
    return render_template('padd.html')

@PET.route('/dprod')
def dprod():
    d = []
    data = list(db1.find({'Animal':'Dog'}))
    for i in data:
        d.append(i)
    print(d)
    return render_template('dog_prod.html',d=d)

@PET.route('/cprod')
def dcat():
    d = []
    data = list(db1.find({'Animal':'Cat'}))
    for i in data:
        d.append(i)
    print(d)
    return render_template('cat_prod.html',d=d)

@PET.route('/tprod')
def dturtle():
    d = []
    data = list(db1.find({'Animal': 'Turtle'}))
    for i in data:
        d.append(i)
    print(d)
    return render_template('tprod.html',d=d)

@PET.route('/bprod')
def bprod():
    d = []
    data = list(db1.find({'Animal': 'Bird'}))
    for i in data:
        d.append(i)
    print(d)
    return render_template('bprod.html',d=d)

@PET.route('/usernav')
def usernav():
    return render_template('usernav.html')

@PET.route('/orders',methods = ['GET','POST'])
def orders():
    pass
    return render_template('myorders.html')

@PET.route('/check',methods = ['GET','POST']) 
def check():
        
    c2=[]
    if 'email' in session:
        bemail=session["email"] 
        data=list(db2.find({'bemail':bemail}))
        sum=list(db2.aggregate([{"$group":{"_id": 0,"TotalPrice": { "$sum": "$subtotal"}}}]))
        for i in data:
            c2.append(i)
        id=db3.insert_one({
            'bemail':bemail,
            # 'Products':d,
            'pid': 1,
            'Discount':0,
            'Total_Price':sum[0]["TotalPrice"]})


        c1=[]
        data=list(db2.find({}))
        for i in data:
            c1.append(i)
        oinsert = db4.insert_one({
            'bemail':bemail,
            'Animal':c1[0]['Animal'],
            'Breed':c1[0]['Breed'],
            'Product_Name':c1[0]['Product_Name'],
            'Product_Type':c1[0]['Product_Type'],
            'Price':c1[0]['Price'],
            'Quantity':c1[0]['count'],
            'Discount':c1[0]['Discount'],
            'Subtotal': sum[0]["TotalPrice"]})
        db4.insert_many([{oinsert}])
    return render_template('checkout.html',c1=c1,c2=c2,sum=sum)

@PET.route('/buy',methods = ['GET','POST'])
def buy():
    db1.update_one({})
    db2.delete_one({'email': session['email']})

    return render_template('buy.html')

@PET.route('/cupdate/<id>',methods = ['GET','POST'])
def cupdate(id):
    if flask.request.method=="POST":
        db2.update_one({"_id":ObjectId(id)},{"$set":{"count":flask.request.form['count']}})
        db2.update_many({}, [ {"$set":{ "count" : {"$toInt": "$count"}}} ],True)
        d=flask.request.form['count']
        l=list(db2.find({"_id":ObjectId(id)},{"subtotal": {"$multiply":["$count","$Price"]}}))
        l1=l[0]['subtotal']
        db2.update_one({"_id":ObjectId(id)},{"$set":{"subtotal":l1}})
        db2.update_one({"_id":ObjectId(id)},{"$set":{"count":flask.request.form['count']}})
        db2.update_many({}, [ {"$set":{ "count" : {"$toInt": "$count"}}} ],True)
        return redirect(url_for('cart1'))

@PET.route('/cart1',methods = ['GET','POST'])
def cart1():
    c1=[]
    if 'email' in session:
        data=list(db2.find({}))
        for i in data:
            c1.append(i) 
    return render_template('cart.html',c1=c1)

@PET.route('/shopping',methods = ['GET','POST'])
def shopping():
    return render_template('shopping.html')

# @PET.route('/cupdate/<id>',methods = ["GET","POST"])
# def cupdate(id):
#     if flask.request.method == "POST":
#         a=flask.request.form.get('count')
#         print(a)
#         db2.update_one({{"_id":ObjectId(id)},{"$set":{"count":a}}})
#         return redirect(url_for('cart1'))

@PET.route('/profile')
def profile():
    return render_template('profile.html')

@PET.route('/cart/<id>',methods = ['GET','POST'])
def cart(id):
    c=[]
    c1=[]
    bemail=session["email"]
    if 'email' in session:
        cdata = list(db1.find({"_id":ObjectId(id)}))
        for i in cdata:
            c.append(i)
        c1data = list(db1.find({"_id":ObjectId(id)},{"Product_Id":1}))
        pcid=c1data[0]["Product_Id"]
        ddata = list(db2.find({},{"_id":0,"Product_Id":1}))
        print(ddata)
        if(ddata!=[]):
            for i in ddata:
                for j in i.values():
                    print(j)
                    print(pcid)
                    if j==pcid:
                        flash("Product already added to cart")
                        return redirect(url_for('cart1'))
            else:
                id=db2.insert_one({
                        'bemail':bemail,
                        'cid': ObjectId(id),
                        'Animal': c[0]['Animal'],
                        'Breed':c[0]['Breed'],
                        'Product_Id': c[0]['Product_Id'],
                        'Product_Name': c[0]['Product_Name'],
                        'Product_Type': c[0]['Product_Type'],
                        'Price':c[0]['Price'],
                        'subtotal':c[0]['Price'],

                        'Discount':c[0]['Discount'],
                        'count':1
                     })
        id=db2.insert_one({
                        'bemail':bemail,
                        'cid': ObjectId(id),
                        'Animal': c[0]['Animal'],
                        'Breed':c[0]['Breed'],
                        'Product_Id': c[0]['Product_Id'],
                        'Product_Name': c[0]['Product_Name'],
                        'Product_Type': c[0]['Product_Type'],
                        'Price':c[0]['Price'],
                        'Discount':c[0]['Discount'],
                        'count':1
                     })
        db2.update_many({}, [ {"$set":{ "Price" : {"$toInt": "$Price"}}} ],True)


    return redirect(url_for('cart1'))

if __name__ == "__main__":
    PET.run(debug=True,port=2027)