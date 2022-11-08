from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlalchemy

views = Blueprint(__name__, "views")

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
        flash("Login Successful!")
        return redirect(url_for("views.user"))
    else:
        if "user" in session:
            flash("Arleady logged in")
            return redirect(url_for("views.user"))

        return render_template("login.html")

@views.route("/user", methods=["POST", "GET"])
def user():
    if "user" in session:
        user = session["user"]
        #return f"<h1>{user}</h1>"

        if request.method == "POST":
            user_email = request.form["user_email"]
            session["user_email"] = user_email
        else:
            if "user_email" in session:
                user_email = session["user_email"]
            else:
                user_email = ""

        return render_template("user.html", email=user_email)
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