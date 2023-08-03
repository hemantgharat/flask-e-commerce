from flask import Flask,request,render_template,redirect,session
import mysql.connector as m
from werkzeug.utils import secure_filename
from datetime import datetime
import sys,time

app=Flask(__name__)
app.secret_key="hii"
@app.route("/")
def home():
    un=""
    if "uname" in session:
        un=session["uname"]
    return render_template('index.html',un=un)

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/Signup")
def reg():
    return render_template('reg.html')

@app.route("/signin",methods=['GET','POST'])
def signin():
    r=""
    msg=""
    if request.method=="POST":
        un=request.form["n"]
        ps=request.form["p"]
        if un=="Admin" and ps=="123":
            session["loggedin"]=True
            session["un"]=un
            return render_template('temp.html')
        else:
            cur=con.cursor()
            cur.execute("select * from register where uname='"+un+"' and password='"+ps+"'")
            rs=cur.fetchone()
            if(rs!=None):
                session["loggedin"]=True
                session["un"]=un
                return render_template('master.html')
            else:
                msg="Please enter valid Username and Password"
        return render_template('index.html', msg = msg)    

@app.route("/register",methods=['GET','POST'])
def addUser():
    if request.method=="POST":
        cur=con.cursor()
        n=request.form["n"]
        p=request.form["p"]
        e=request.form["e"]
        m=request.form["m"]
        c=request.form["c"]
        pc=request.form["pc"]
        cur.execute("insert into register values(null,'"+n+"','"+p+"','"+e+"',"+m+",'"+c+"',"+pc+")")
        con.commit()
        return ("/login")

@app.route("/addProd")
def addprod():
    cur=con.cursor()
    cur.execute("select * from category")
    cats=cur.fetchall()
    con.commit()
    return render_template("addProd.html",cats=cats)

@app.route("/addProd",methods=['GET','POST'])
def addproduct():
    if request.method=="POST":
        cur=con.cursor()
        f=request.files['im']
        f.save("static\\images\\"+secure_filename(f.filename))
        cur.execute("insert into product values(null,'"+request.form["n"]+"','"+request.form["d"]+"',"+request.form["pr"]+",'"+f.filename+"',"+request.form["cid"]+","+request.form["q"]+")")
        con.commit()
        return render_template('/products.html')

@app.route("/products")
def showproduct():
    cur=con.cursor()
    cur.execute("select * from product")
    prods=cur.fetchall()
    con.commit()
    return render_template('products.html',prods=prods)

@app.route("/deleteProd",methods=['GET','POST'])
def delprod():
    if request.method=="POST":
        cur=con.cursor()
        cur.execute("delete from product where pid="+request.form["pid"])
        con.commit()
        return render_template("/admin.html")

@app.route("/AddCat")
def addcate():
    cur=con.cursor()
    cur.execute("select * from category")
    cats=cur.fetchall()
    con.commit()
    return render_template("AddCat.html",cats=cats)

@app.route("/AddCat",methods=['GET','POST'])
def addcategory():
    if request.method=="POST":
        cur=con.cursor()
        cur.execute("insert into category(cname) values('"+request.form["cn"]+"')")
        con.commit()
        return render_template('/Showcat.html')

@app.route("/Showcat")
def Showcategory():
    cur=con.cursor()
    cur.execute("select * from category")
    cats=cur.fetchall()
    con.commit()
    return render_template('Showcat.html',cats=cats)

@app.route("/Editcat")
def editcat():
    cid=request.args["cid"]
    cur=con.cursor()
    cur.execute("select * from category where cid="+cid)
    c=cur.fetchone()
    con.commit()
    return render_template("Editcat.html",c=c)


@app.route("/editcategory",methods=['GET','POST'])
def editcc():
    if request.method=="POST":
        cur=con.cursor()
        cur.execute("Update category set cname='"+request.form["cn"]+"' where cid="+request.form["id"])
        con.commit()
        return render_template('/Showcat.html')

@app.route("/delcat",methods=['GET','POST'])
def delcat():
    if request.method=="POST":
        cur=con.cursor()
        cur.execute("delete from category where cid="+request.form["cid"])
        con.commit()
        return render_template("/admin.html")


@app.route("/search")
def serachprod():
    n=request.args["search"]
    cur=con.cursor()
    cur.execute("select * from product where pname like '%"+n+"%' or pdesc like '%"+n+"%' or cid =(select cid from category where cname like '%"+n+"%')")
    prds=cur.fetchall()
    return render_template("ShowProds.html",pds=prds)

@app.route("/users")
def showuser():
    cur=con.cursor()
    cur.execute("select * from register")
    user=cur.fetchall()
    con.commit()
    return render_template('users.html',user=user)

@app.route("/deleteuser",methods=['GET','POST'])
def deluser():
    if request.method=="POST":
        cur=con.cursor()
        cur.execute("delete from register where rid="+request.form["uid"])
        con.commit()
        return render_template("/users.html")    

@app.route("/Feedback")
def feedbck():
    cur=con.cursor()
    cur.execute("select * from feedback")
    feed=cur.fetchall()
    con.commit()
    return render_template("Feedback.html",feed=feed)

@app.route("/Feedback",methods=['GET','POST'])
def fb():
    if request.method=="POST":
        cur=con.cursor()
        cur.execute("insert into feedback values('"+request.form["n"]+"','"+request.form["d"]+"','"+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"')")
        con.commit()
        return render_template("/index.html")

@app.route("/showFB")
def feedback():
    cur=con.cursor()
    cur.execute("select * from feedback")
    feed=cur.fetchall()
    con.commit()
    return render_template('showFB.html',feed=feed)

@app.route("/allProd")
def allProd1():
        cur=con.cursor()
        cur.execute("select pid,pname,pdesc,price,p_img from product")
        prods=cur.fetchall()
        con.commit()
        return render_template('allProd.html',prods=prods)

@app.route("/addToCart",methods=['GET','POST'])
def add_to_cart():
    if request.method=="POST":
        cur=con.cursor()
        f=request.files['im']
        f.save("static\\images\\"+secure_filename(f.filename))
        cur.execute("insert into cart values(null,'"+request.form["n"]+"','"+request.form["d"]+"',"+request.form["pr"]+",'"+f.filename+"',"+request.form["cid"]+")")
        prod=cur.fetchall()
        con.commit()
        return render_template('allProd.html')


@app.route("/contact")
def conc():
    return render_template('contact.html')

@app.route("/temp")
def hm():
    return render_template('temp.html')

if __name__=='__main__':
    global con
    con=m.connect(host="localhost",
                database='Project_1',
                charset="utf8",
                user="root",
                password="")
    app.run(debug=True)