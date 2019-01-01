from __future__ import print_function
from flask import Flask, flash, redirect, render_template, request, session, url_for

from helpers import apology
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode





conn = mysql.connector.connect(host='retailapp.chhkxmzfw1fy.us-east-1.rds.amazonaws.com', port=3306, user='admin1', passwd='Veri1899$', db='retaildb')


db = conn.cursor(prepared=True)



app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="80")
