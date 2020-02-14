
from bs4 import BeautifulSoup

s ='''<div class="col-md-3">          
            <div class="panel panel-primary">
    <div class="panel-heading">
        <h3 class="panel-title">文章分类</h3>
    </div>
    <div class="panel-body">
        
            <p><a href="">生活(1)</a></p>
        
            <p><a href="">技术(3)</a></p>
            <script src="/static/jquery-3.4.1.js"></script>
            <link rel="stylesheet" href="/static/bootstrap/css/bootstrap.min.css">'''

bs = BeautifulSoup(s, "html.parser")
print(bs.text)  # 放内容简介里的
print('*'*100)
print(bs.text.replace("\n", ""))
print('*'*100)

for tag in bs.find_all():
    if tag.name in ["script", "link"]:
        # 清除标签
        print("清除的标签:", tag)
        tag.decompose()
print('*'*100)
print(str(bs))  # 放类容详情里的
