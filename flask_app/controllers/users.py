from crypt import methods
from flask_app import app
from flask import render_template, redirect, request, session
#import model that you need below
from flask_app.models.user import User


@app.route("/")
def index():
    all_users=User.get_all_friendships()
    all_people=User.get_all()
    return render_template("index.html", all_users=all_users, all_people=all_people)

@app.route("/new_user", methods={"POST"})
def new_user():
    User.save(request.form)
    return redirect("/")
@app.route("/create_friendship", methods=["POST"])
def new_friends():
    if not User.validate_friendship(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    User.new_friend(request.form)
    return redirect("/")