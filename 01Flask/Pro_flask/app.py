from flask import Flask, render_template, redirect, url_for, request, session, Markup, current_app, g
from werkzeug import run_simple
app = Flask(__name__)
print(app.config.items())  # 查看所有配置文件
app.config.from_object("settings.TestingConfig")  # 选择使用配置文件
app.secret_key = 'dsfsadf'  # session加盐
STUDENT_DICT = {
    1: {'name': "xiaoli", 'pwd': "123", 'age': 21},
    2: {'name': "laoxiao", 'pwd': "123", 'age': 22},
    3: {'name': "baoquan", 'pwd': "123", 'age': 23},
}


@app.template_global()  # 相当于在全局返回了一个函数,模板可以通过替换去使用
def add(a1, a2):
    return a1 + a2


@app.route("/test")
def test():
    ret_dict = {
        'txt': Markup("<input type='text' />"),  # 相当于Django(mark_safe)
        'users': ["xiaoli", "laoxiao"]
    }

    return render_template("test.html", **ret_dict)


@app.before_request  # 相当于Django的中间件(执行视图函数之前进行操作)
def authlogin():
    if request.path == "/login":
        return None
    if not session.get("user"):
        return redirect(url_for('login'))


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    username = request.form.get("username")  # 相当于Django(request.GET)
    pwd = request.form.get("pwd")
    if username == "xiaoli" and pwd == "123":
        session["user"] = username
        return redirect(url_for("index"))
    return render_template("login.html", error_msg='用户名密码错误')


@app.route('/index', endpoint='index')  # 相当于Django(url里的 name),用于 url_for反向解析, 默认就是函数名
def index():
    return render_template("index.html", stu_dict=STUDENT_DICT)


@app.route('/delete/<int:nid>')  # nid 是int类型
def delete(nid):
    del STUDENT_DICT[nid]
    return redirect(url_for('index'))  # 相当于Django的路由反向解析(默认是函数名)


@app.route('/detail/<int:nid>')
def detail(nid):
    info = STUDENT_DICT[nid]
    return render_template("detail.html", info=info)


if __name__ == '__main__':
    app.run()
