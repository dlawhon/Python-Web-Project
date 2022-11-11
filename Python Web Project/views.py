from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from static.classes import sqlServerConnect

import pyodbc

views = Blueprint(__name__, "views")

cursor, conn = sqlServerConnect()

@views.route("/")
def home():
    return render_template("index.html", name="Tim")

#@views.route("/profile/<username>")
#def profile(username):
    #return render_template("index.html", name=username)


#@views.route("/profile")
#def profile():
    #args = request.args
    #name = args.get('name')
    #return render_template("index.html", name=name)

@views.route("/orders")
def orders():
    return render_template("orders.html")

@views.route("/invoices")
def invoices():
    return render_template("invoices.html")

@views.route("/profile")
def profile():
    return render_template("profile.html")

@views.route("/go-to-home")
def go_to_home():
    return redirect(url_for("views.home"))

@views.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["username"]
        session["user"] = user

        #How to query the database with sqlalchemy
        #found_user = users.query.filter_by(name=user).first()


       # if found_user:
            #session["email"] = found_user.email
       # else:
            #How to add a record to the database with sqlalchemy
            #addUser = users(user, "")
            #db.session.add(addUser)
            #db.session.commit()

        flash("Login Successful!")
        return redirect(url_for("views.user"))
    else:
        if "user" in session:
            flash("Arleady logged in")
            return redirect(url_for("views.user"))

        return render_template("login.html")

@views.route("/user", methods=["POST", "GET"])
def user():
    user_email = None
    if "user" in session:
        user = session["user"]
        #return f"<h1>{user}</h1>"

        if request.method == "POST":
            user_email = request.form["user_email"]
            session["user_email"] = user_email

            #How to update a record in the database with sqlalchemy
            #found_user = users.query.filter_by(name=user).first()
            #found_user.email = user_email
            #db.session.commit()

            flash("Email was saved!")
        else:
            if "user_email" in session:
                user_email = session["user_email"]

        return render_template("user.html", email=user_email, user=user)
    else:
        flash("You are not logged in!")
        return redirect(url_for("views.login"))

@views.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"{user} you have been logged out!", "info")

    session.pop("user", None)
    session.pop("user_email", None)
    return redirect(url_for("views.login"))