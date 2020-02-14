from flask import Blueprint, Response, session, render_template, request, redirect, url_for
import os
import uuid
import shutil
from ..utils import helper
import datetime
from settings import Config

ind = Blueprint('ind', __name__)


@ind.before_request  # (执行这个 蓝图 里的视图函数之前 进行操作)
def authlogin():
    if not session.get("user_info"):
        return redirect('/login')


@ind.route("/index", endpoint="index")
def index():
    return render_template("index.html")


@ind.route("/user_list")
def user_list():
    result = helper.fetch_all('select account.id,account.name,account.nickname,sum(count_code.line) as total '
                              'from count_code '
                              'left join account on count_code.account_id = account.id '
                              'group by account.id')
    print(result)
    return render_template("user_list.html", user_list=result)


@ind.route("/detail/<int:nid>")
def detail(nid):
    result = helper.fetch_all('select count_code.id,account.name,count_code.line,count_code.create_date '
                              'from count_code '
                              'left join account on count_code.account_id = account.id '
                              'where account_id=%s', (nid,))
    print(result)
    list = []
    for i in result:
        c_time = i.get("create_date")
        c_time = str(c_time)
        c_time = c_time.replace("-", ",")
        aa, month, cc = c_time.split(',')
        month = int(month)
        if 0 < month <= 12:
            month = month - 1
        new_time = ",".join([aa, str(month), cc])
        print(new_time)
        dict = {
            "id": i.get("id"),
            "name": i.get("name"),
            "create_date": i.get("create_date"),
            "c_time": new_time,
            "line": i.get("line"),
        }
        list.append(dict)
    return render_template("count_code.html", code_list=list)


@ind.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template("upload.html")

    file_obj = request.files.get("code")
    print(file_obj.filename)  # 上传的文件名
    print(file_obj.stream)  # 上传的文件内容

    # 0.判断今日是否上传过
    ctime = datetime.date.today()  # 现在的时间
    c_obj = helper.fetch_all('select create_date from count_code where account_id = %s',
                                (session.get('user_info').get('id')))
    for item in c_obj:
        lib_time = item.get("create_date")
        if lib_time == ctime:
            return render_template("upload.html", msg='今日已上传过文件')

    # 1.检查上传文件后缀名
    name_ext = file_obj.filename.rsplit('.', maxsplit=1)
    if len(name_ext) != 2:
        return "请上传zip压缩文件"
    if name_ext[1] != 'zip':
        return "请上传zip压缩文件"
    """
    # 2. 接受用户上传文件,并写入到本地服务器
    file_path = os.path.join("statistical_code/media", file_obj.filename)  # statistical_code/media/filename
    print(file_path)
    file_obj.save(file_path)  # 上传的文件保存到path拼接的路径中
    # 3. 解压zip文件
    shutil._unpack_zipfile(file_path, 'aaa')
    """
    # 2+3, 接受用户上传文件,并解压到指定目录
    target_path = os.path.join("statistical_code/media", str(uuid.uuid4()))
    shutil._unpack_zipfile(file_obj, target_path)

    # 4.遍历某目录下的所有文件
    count = 0
    for base_path, folder_list, file_list in os.walk(target_path):  # 路径, 文件夹, 文件
        for file_name in file_list:
            file_path = os.path.join(base_path, file_name)
            if not file_path.endswith('py'):  # 不是py文件
                continue
            file_num = 0
            with open(file_path, "rb") as f:
                for line in f:
                    line = line.strip()
                    if not line:  # 是空行
                        continue
                    if line.startswith(b'#'):  # 是注释
                        continue
                    file_num += 1
            count += file_num
            print(file_num, file_path)
    print(count)
    # 5.数据保存入数据库
    account_id = session.get("user_info").get("id")
    print(account_id)
    helper.insert('insert into count_code(account_id,create_date,line) '
                  'values(%s,%s,%s)', (account_id, ctime, count))
    return render_template("upload.html", msg='上传成功共计%s行代码' % count)

