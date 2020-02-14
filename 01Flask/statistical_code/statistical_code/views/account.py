from flask import Blueprint,Response, session, render_template, request, redirect, url_for
from ..utils import md5, helper

account = Blueprint('account', __name__)


@account.route("/index")
def index():
    return render_template("/index.html")


@account.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("/login.html")
    user = request.form.get("username")
    pwd = request.form.get("pwd")
    pwd = md5.md5(pwd)

    # 使用数据库连接池,并使用自己封装的方法
    result = helper.fetch_one('select id,nickname from account where name=%s and pwd=%s', [user, pwd])

    if result:
        session['user_info'] = result
        return redirect('/index')
    return render_template("/login.html", error_msg='用户名密码错误')


@account.route("/logout")
def logout():
    if "user_info" in session:
        del session["user_info"]
        return redirect("/login")
    return redirect("/login")
# @account.route("/reg", methods=["GET", "POST"])
# def reg():
#     if request.method == "GET":
#         return render_template("reg.html")
#     user = request.form.get("username")
#     nick = request.form.get("nickname")
#     pwd = request.form.get("pwd")
