from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_required, current_user
from static.sys import *
from werkzeug.security import generate_password_hash, check_password_hash

import pyodbc

views = Blueprint(__name__, "views")

cursor, conn = sqlServerConnect()

@views.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":

        username = request.form["username"]
        userPassword = request.form["userPassword"]

        userParameters = {
          "userFirstName": None,
          "userLastName": None,
          "username": username,
          "userEmail": None,
          "userPassword": userPassword
        }
 
        results = findUser(username)

        if results:
            #check the password
            if check_password_hash(results.hash, userParameters.get('userPassword')):
                #Maybe?????
                #login_user(user, remember=remember)
                loginUser(results.ID)
            else:
                #The did not provide the correct password
                session.pop('_flashes', None)
                flash("Incorrect Username/Password", "danger")
                return render_template("login.html")
            
        else:
            flash("Incorrect Username/Password", "danger")
            return render_template("login.html")
            #newUser = User(userParameters)

        return redirect(url_for("views.home"))
        #return redirect(url_for("views.user"))
    else:
        if "userName" in session:
            flash("Arleady logged in")
            return redirect(url_for("views.home"))
            #return redirect(url_for("views.user"))

        return render_template("login.html")

@views.route("/register", methods=["POST", "GET"])
def register():
    
    if request.method == "POST":

        userFirstName = request.form["userFirstName"]
        userLastName = request.form["userFirstName"]
        username = request.form["username"]
        userEmail = request.form["userEmail"]
        userPassword = request.form["userPassword"]

        userParameters = {
          "userFirstName": userFirstName,
          "userLastName": userLastName,
          "username": username,
          "userEmail": userEmail,
          "userPassword": userPassword
        }
 
        results = findUser(username)

        if results:
            #This user already exists, they may need to reset their password
            loginUser(results.ID)
        else:
            newUser = User(userParameters)

        return redirect(url_for("views.home"))
    else:
        #if "userName" in session:
            #flash("Arleady logged in")
        return render_template("register.html")
            #return redirect(url_for("views.user"))

    #return render_template("register.html")



    
#Maybe?????
#login_manager = LoginManager()
#login_manager.login_view = 'views.login'
#login_manager.init_app(app)





@views.route("/", methods=['GET', 'POST'])
#@login_required
def home():
    if checkSession() is False:
        return redirect(url_for("views.login"))
    else:
        return render_template("index.html")

@views.route("/charts")
def charts():
    if checkSession() is False:
        return redirect(url_for("views.login"))
    else:
        return render_template("charts.html")

@views.route("/cards")
def cards():
    if checkSession() is False:
        return redirect(url_for("views.login"))
    else:
        return render_template("cards.html")

@views.route("/buttons")
def buttons():
    if checkSession() is False:
        return redirect(url_for("views.login"))
    else:
        return render_template("buttons.html")

@views.route("/tables")
def tables():
    if checkSession() is False:
        return redirect(url_for("views.login"))
    else:
        return render_template("tables.html")

@views.route("/forgot-password")
def forgot_password():
    return render_template("forgot-password.html")

@views.route("/404")
def error():
    if checkSession() is False:
        return redirect(url_for("views.login"))
    else:
        return render_template("404.html")

@views.route("/blank")
def blank():
    if checkSession() is False:
        return redirect(url_for("views.login"))
    else:
        return render_template("blank.html")

@views.route("/utilities-animation")
def utilities_animation():
    if checkSession() is False:
        return redirect(url_for("views.login"))
    else:
        return render_template("utilities-animation.html")

@views.route("/utilities-border")
def utilities_border():
    if checkSession() is False:
        return redirect(url_for("views.login"))
    else:
        return render_template("utilities-border.html")

@views.route("/utilities-color")
def utilities_color():
    if checkSession() is False:
        return redirect(url_for("views.login"))
    else:
        return render_template("utilities-color.html")

@views.route("/utilities-other")
def utilities_other():
    if checkSession() is False:
        return redirect(url_for("views.login"))
    else:
        return render_template("utilities-other.html")

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
        return True

@views.route("/logout")
def logout():
    if "userName" in session:
        user = session["userName"]
        flash(f"{user} you have been logged out!", "info")

    logoutUser()
    return redirect(url_for("views.home"))
