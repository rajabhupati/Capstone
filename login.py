from flask import Flask, session, redirect, url_for, escape, request, render_template
from flask_session import Session
from hashlib import md5
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from tempfile import mkdtemp
from helpers import apology, login_required
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

if __name__ == '__main__':
     
    db = mysql.connector.connect(host='retailapp.chhkxmzfw1fy.us-east-1.rds.amazonaws.com', port=3306, user='admin1', passwd='Veri1899$', db='retaildb')
    cur = db.cursor()

class ServerError(Exception):pass


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


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


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
        db.execute(sql,insert_tuple) 
	conn.commit()
	print("record inserted.")
	return render_template("sucess.html")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        product = request.form.get("product")
        rows = db.execute("Select * from products where product_name= :name", name = product)
        if not rows[0]["product_name"]:
            return apology("Product does not exists")
        quantity= int(request.form.get("quantity"))
        if quantity<0:
            return apology("Enter valid quantity")
        if (quantity > rows[0]["product_stock"]):
            return apology("Stock not available")
        else:
            cash = db.execute("Select cash from users where id=:id", id=session["user_id"])
            if not cash or float(cash[0]["cash"] < float(rows[0]["product_price"])):
                return apology("Not enough cash")
        db.execute("Update users set cash = cash - :bought where id = :id", bought= rows[0]["product_price"], id=session["user_id"])
        flash('Bought')
        db.execute("insert into invoice(inv_date, total, product_id, user_id) values (datetime('now', 'localtime'), :total, :p_id, :id)", total =  rows[0]["product_price"], p_id=rows[0]["product_id"], id=session["user_id"])

        db.execute("Update products set product_stock = product_stock - :count where product_name=:name", name=product, count=quantity)
        return redirect(url_for("index"))
    else:
        return render_template("buy.html")

@app.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    if request.method == "GET":
        rows = db.execute("select * from cart where user_id = :id", id=session["user_id"])
        return render_template("cart.html", items=rows)
    else:
        rows = db.execute("select * from cart where user_id = :id", id=session["user_id"])
        for item in rows:

            prod = db.execute("select * from products where product_id= :id", id = item["product_id"])
            if int((prod[0]["product_stock"])) < 1:
                return apology("Stock Finished")
            cash = db.execute("Select cash from users where id=:id", id=session["user_id"])
            if not cash or float(cash[0]["cash"] < float(prod[0]["product_price"])):
                return apology("Not enough cash")
            db.execute("Update users set cash = cash - :bought where id = :id", bought= float(prod[0]["product_price"] * item["quantity"]) , id=session["user_id"])
            flash('Bought')
            db.execute("insert into invoice(inv_date, total, product_id, user_id) values (datetime('now', 'localtime'), :total, :p_id, :id)", total =  prod[0]["product_price"]* item["quantity"], p_id=prod[0]["product_id"], id=session["user_id"])
            db.execute("Update products set product_stock = product_stock - :count where product_name=:name", count=item["quantity"], name = prod[0]["product_name"] )
            db.execute("Delete from cart where user_id = :id", id=session["user_id"])
        return render_template("cart.html")






if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=80)
