from flask import Blueprint, render_template, request, redirect, url_for

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

@views.route("/profile")
def profile():
    return render_template("profile.html")

@views.route("/go-to-home")
def go_to_home():
    return redirect(url_for("views.home"))