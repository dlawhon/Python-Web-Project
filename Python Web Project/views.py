from flask import Blueprint, render_template, request, redirect, url_for, session, flash
#from static.classes import sqlServerConnect
from static.sys import *

import pyodbc

views = Blueprint(__name__, "views")

cursor, conn = sqlServerConnect()

@views.route("/")
def home():
    if checkSession() is False:
        return redirect(url_for("views.login"))
    else:
        return render_template("index.html", name="Tim")

@views.route("/orders")
def orders():
    if checkSession() is False:
        return redirect(url_for("views.login"))
    else:
        return render_template("orders.html")

@views.route("/invoices")
def invoices():
    if checkSession() is False:
        return redirect(url_for("views.login"))
    else:
        return render_template("invoices.html")

@views.route("/profile")
def profile():
    if checkSession() is False:
        return redirect(url_for("views.login"))
    else:
        return render_template("profile.html")

@views.route("/go-to-home")
def go_to_home():
    if checkSession() is False:
        return redirect(url_for("views.login"))
    else:
        return redirect(url_for("views.home"))

@views.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":

        user = request.form["username"]
 
        results = findUser(user)

        if results:
            loginUser(results.ID)
        else:
            newUser = User(user)

        return redirect(url_for("views.user"))
    else:
        if "userName" in session:
            flash("Arleady logged in")
            return redirect(url_for("views.user"))

        return render_template("login.html")

@views.route("/user", methods=["POST", "GET"])
def user():
    user_email = None
    if "userName" in session:
        user = session["userName"]
        #return f"<h1>{user}</h1>"

        if request.method == "POST":
            user_email = request.form["user_email"]
            session["userEmail"] = user_email

            #How to update a record in the database with sqlalchemy
            #found_user = users.query.filter_by(name=user).first()
            #found_user.email = user_email
            #db.session.commit()

            flash("Email was saved!")
        else:
            if "userEmail" in session:
                user_email = session["userEmail"]

        return render_template("user.html", email=user_email, user=user)
    else:
        flash("You are not logged in!")
        return redirect(url_for("views.login"))

@views.route("/logout")
def logout():
    if "userName" in session:
        user = session["userName"]
        flash(f"{user} you have been logged out!", "info")

    #session.pop("userName", None)
    #session.pop("userEmail", None)
    logoutUser()
    return redirect(url_for("views.login"))
