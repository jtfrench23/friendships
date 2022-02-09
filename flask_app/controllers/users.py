from crypt import methods
from flask_app import app
from flask import render_template, redirect, request, session
#import model that you need below
from flask_app.models import user

# Create
@app.route("/new_user", methods={"POST"})
def new_user():
    if not user.User.validate_user(request.form):
        return redirect('/')
    user.User.save(request.form)
    return redirect("/")
@app.route("/create_friendship", methods=["POST"])
def new_friends():
    if not user.User.validate_friendship(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    user.User.new_friend(request.form)
    return redirect("/")

#READ
@app.route("/")
def index():
    all_users= user.User.get_all_friendships()
    all_people= user.User.get_all()
    return render_template("index.html", all_users=all_users, all_people=all_people)

#UPDATE

#DELETE




