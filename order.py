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

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    session_username="raja"
    bought=rows[0]["product_price"]
    if request.method == "POST":
        product = request.form.get("product")
        rows = db.execute("Select * from products where product_name= %s;", [product])
        if not rows[0]["product_name"]:
            return apology("Product does not exists")
        quantity= int(request.form.get("quantity"))
        if quantity<0:
            return apology("Enter valid quantity")
        if (quantity > rows[0]["product_stock"]):
            return apology("Stock not available")
        else:
            cash = db.execute("Select cash from users where username=%s;", [session_username])
            if not cash or float(cash[0]["cash"] < float(rows[0]["product_price"])):
                return apology("Not enough cash")
        db.execute("Update users set cash = cash - %s where username = %s;", [bought], [session_username])
        flash('Bought')
        db.execute("insert into invoice(inv_date, total, product_id, username) values (datetime('now', 'localtime'), :total, :p_id, :id)",rows[0]["product_price"],rows[0]["product_id"], [session_username])

        db.execute("Update products set product_stock = product_stock - %s where product_name=%s", [quantity],[product])
        return redirect(url_for("index"))
    else:
        return render_template("buy.html")
                                              


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="80")

