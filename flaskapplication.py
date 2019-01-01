from __future__ import print_function
from flask import Flask, flash, redirect, render_template, request, session, url_for

from helpers import apology
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode





conn = mysql.connector.connect(host='retailapp.chhkxmzfw1fy.us-east-1.rds.amazonaws.com', port=3306, user='admin1', passwd='Veri1899$', db='retaildb')


db = conn.cursor()



app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Test 123 "

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
        print(username)
        # insert the new user into users, storing the hash of the user's password
        result = db.execute("INSERT INTO users (username, hash, cash, contact_number, address) VALUES(:username, :hash, :cash, :contact_number, :address)",
                            username=request.form.get("username"),
                            hash=request.form.get("password"),
                            cash=request.form.get("cash"),
                            contact_number= request.form.get("contact"),
                            address=request.form.get("address")
                            )

        if not result:
            return apology("Username already exist")

        # remember which user has logged in
        session["user_id"] = result

        # redirect user to home page
        return redirect(url_for("index"))

    else:
        return render_template("register.html")




if __name__ == "__main__":
    app.run(host="0.0.0.0", port="80")
