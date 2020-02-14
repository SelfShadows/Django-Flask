from flask import Blueprint, Response, session, render_template, request, redirect, url_for


my_tmp = Blueprint('tmp', __name__)


@my_tmp.route("/home")
def home():

    return render_template("tmp/home.html")