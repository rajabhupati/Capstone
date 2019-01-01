from flask import Flask, session, redirect, url_for, escape, request, render_template,flash
from flask_session import Session
from hashlib import md5
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from tempfile import mkdtemp
from helpers import apology, login_required
import os
import datetime
app = Flask(__name__)
app.secret_key = os.urandom(12)
if __name__ == '__main__':
     
    db = mysql.connector.connect(host='retailapp.chhkxmzfw1fy.us-east-1.rds.amazonaws.com', port=3306, user='admin1', passwd='Veri1899$', db='retaildb',autocommit=True)
    cur = db.cursor(buffered=True)

class ServerError(Exception):pass

@app.route("/")
def hello_world():
    return render_template("register.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
      # ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password")

        # ensure password and verified password is the same
        elif request.form.get("password") != request.form.get("passwordagain"):
            return apology("password doesn't match")

        elif not request.form.get("contact"):
            return apology("Must provide Contact")
        elif not request.form.get("address"):
            return apology("Must provide Address")
        elif not request.form.get("cash"):
            return apology("Must provide cash")
        username=request.form.get("username")
        hash=request.form.get("password")
        cash=request.form.get("cash")
        contact= request.form.get("contact")
        address=request.form.get("address")


        sql="""INSERT INTO users (username, hash, cash, contact_number, address) VALUES (%s,%s,%s,%s,%s)"""
        insert_tuple = (username,hash,cash,contact,address)
        cur.execute(sql,insert_tuple)
        db.commit()
        print("record inserted.")
        return render_template("sucess.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if 'username' in session:
        return redirect(url_for('index'))

    error = None
    try:
        if request.method == 'POST':
            username_form  = request.form['username']
            cur.execute("SELECT COUNT(1) FROM users WHERE username = %s;",[username_form])

            if not cur.fetchone()[0]:
                raise ServerError('Invalid username')

            password_form  = request.form['password']
            cur.execute("SELECT hash FROM users WHERE username = %s;",[password_form])

            for row in cur.fetchall():
                if md5(password_form).hexdigest() == row[0]:
                    session['username'] = request.form['username']
                    return redirect(url_for('index'))

            raise ServerError('Invalid password')
    except ServerError as e:
        error = str(e)
    return render_template('login.html', error=error)



@app.route("/buy", methods=["GET", "POST"])
def buy():
    session_username='raja'
    if request.method == 'POST':
        product = request.form['product']
	cur.execute("Select product_id,product_name,product_price,product_stock from products where product_name=%s;", [product])
  	prdt=cur.fetchone()
	prod_id=prdt[0]
        product_stock=prdt[3]
	product_price=prdt[2]
	if prdt== None:
            return ServerError("Product does not exists")
        quantity= int(request.form["quantity"])
        print("productid,product_stock,product_price",prod_id,product_stock,product_price)
	if quantity<0:
            return ServerError("Enter valid quantity")
        if (quantity > product_stock):
            return apology("Stock not available")
        else:
            cur.execute("Select cash from users where username=%s;", [session_username])
	    cash=cur.fetchone()
            bought=float(product_price)*float(quantity)
            print(" bought",bought)
            if not cash or float(cash[0]< bought):
                return ServerError("Not enough cash")
        new_cash=float(cash[0])-float(bought)
        print("new_cash",new_cash)
        deduct_sql=("""Update users set cash = %s where username=%s""")
        data_cash=(new_cash,session_username)
	cur.execute(deduct_sql,data_cash)
        x=datetime.datetime.now()
	print(x)
        print(session_username)
	inv_insert=("""insert into invoice(inv_date, total, product_id, username) values (%s, %s, %s, %s)""")
	data_inv=(x,bought,prod_id,session_username)
        cur.execute(inv_insert,data_inv)
	new_q=int(product_stock)-int(quantity)
        print("new_q",new_q)
	product_sql=("""update products set product_stock = %s where product_name=%s""")
	data_product=(new_q,product)
        cur.execute(product_sql,data_product) 
        print("data is inserting")
        print("data_cash data_inv product",data_cash,data_inv,product)
	db.commit()
	return redirect(url_for("login"))
    else:
        return render_template("buy.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)
