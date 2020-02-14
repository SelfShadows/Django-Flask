from django.test import TestCase

# Create your tests here.


class Person(object):
    def foo(self):
        print("111")

    def run(self):
        print("run")

p1 = Person()
a = getattr(p1, "foo")
setattr(p1, "foo", p1.run)  # 使调用p1.foo 方法 变成调用 p1.run 方法
p1.foo()

aa = {"k1": "v1", "k2": "v2", "k3": "v3"}
bb = [v for k, v in aa.items()]  # 列表推导式 添加数据
print(bb)

cc = 11
dd = 5 if cc==12 else 13  # 三元判断
print(dd)

ee = [1, 2, 3, 4]
print(ee[-3])
